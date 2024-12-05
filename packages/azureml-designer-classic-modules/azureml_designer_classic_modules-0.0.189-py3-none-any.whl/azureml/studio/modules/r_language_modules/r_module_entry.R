check_and_import <- function(packages){
  tryCatch({
      for(package in packages){
        if(!require(package, character.only = TRUE)){
          library(package, character.only = TRUE)
        }
      }
    }, error = function(e) {
    stop(sprintf("Initialize R script execution environment failed. Reason: %s.", toString(e)))
  })
}

convert_to_list <- function(results){
  result_class = class(results)
  if (result_class == "list"){
    return(results)
  } else {
    return(list(dataset1=results))
  }
}

convert_column_types <- function(schema_path, dataframe){
  if(file.exists(schema_path)){
    schema_json = fromJSON(schema_path)

    # Get origin column types from _schema.json
    col_origin_types <- schema_json$columnAttributes$type
    names(col_origin_types) <- schema_json$columnAttributes$name

    col_cur_types <- lapply(dataframe, class)
    col_names <- names(col_cur_types)

    set_col_type_count = 0
    for (col_name in col_names)
    {
      col_cur_type <- col_cur_types[col_name]
      # "list" means the column doesn't have a specific column type like "numeric" and "as.character"
      # which is similar as the "object" type in Python dataframe.
      # "list" column can't work well with some R libraries, like data.table.
      # So, we should fix the column type by using our schema.json file

      origin_type = col_origin_types[col_name]
      if ("list" == col_cur_type) {

        if ("Numeric" == origin_type || "NAN" == origin_type)
        {
          dataframe[col_name] <- dataframe[col_name] %>% replace(.=="NULL", NA)
          dataframe[col_name] <- lapply(dataframe[col_name], as.numeric)
          set_col_type_count = set_col_type_count + 1
        }
        else if ("String" == origin_type)
        {
          dataframe[col_name] <- lapply(dataframe[col_name], as.character)
          set_col_type_count = set_col_type_count + 1
        }
        else if ("Categorical" == origin_type)
        {
          dataframe[col_name] <- lapply(dataframe[col_name], as.character)
          dataframe[col_name] <- lapply(dataframe[col_name], as.factor)
          set_col_type_count = set_col_type_count + 1
        }
        else if ("Binary" == origin_type)
        {
          dataframe[col_name] <- dataframe[col_name] %>% replace(.=="NULL", FALSE)
          dataframe[col_name] <- lapply(dataframe[col_name], as.logical)
          set_col_type_count = set_col_type_count + 1
        }
      } else if ("Categorical" == origin_type & sapply(dataframe[col_name], class) == "character") {
        # Recover category type because category type-info is lost in
        # _uncategorize_categorical_column in execute_r_script.py.
        # This recovery operation is only applied to string column, because convert column to factor type will
        # lead to underlying values converted to string values; this type change needs to be avoided.
        dataframe[col_name] <- lapply(dataframe[col_name], as.factor)
        set_col_type_count = set_col_type_count + 1
      }
    }

    print(sprintf("%d columns have been set to origin types.", set_col_type_count))
  }

  return (dataframe)
}

load_dataframe_from_parquet <- function(parquet_path, schema_path){
  if(file.exists(parquet_path)){
    r_dataframe <- pd$read_parquet(parquet_path, "pyarrow")
    r_dataframe <- convert_column_types(schema_path, r_dataframe)
  } else {
    r_dataframe <- NULL
  }

  return(r_dataframe)
}

save_dataframe_to_parquet <- function(r_dataframe, parquet_path, output_schema_path){
  class_str = class(r_dataframe)
  if (is.data.frame(r_dataframe) || any(grepl("pandas.core.frame.DataFrame", class_str))) {
    py_dataframe <- r_to_py(r_dataframe)
    py_dataframe$to_parquet(parquet_path, "pyarrow")

    py_dataframe_schema = azureml$studio$core$data_frame_schema$DataFrameSchema$data_frame_to_dict(py_dataframe)
    azureml$studio$core$utils$jsonutils$dump_to_json_file(py_dataframe_schema, output_schema_path)
  } else if (is.null(r_dataframe)) {
    warning(sprintf("Skip output: '%s' since it's NULL.", parquet_path))
  } else {
    stop(sprintf("Unsupported return type, expect: 'data.frame' or 'pandas.core.frame.DataFrame', actual: '%s'", class_str))
  }
}

# Function get_current_run() and upload_files_to_run() are copied from Azure ML SDK for R
# Currently, the SDK can only be installed in R code
# Will remove the code copy when it's available in Conda
# Source code repository: https://github.com/Azure/azureml-sdk-for-r
get_current_run <- function(allow_offline = TRUE) {
  azureml$core$run$Run$get_context(allow_offline)
}

upload_files_to_run <- function(names, paths, timeout_seconds = NULL,
                                run = NULL) {
  if (is.null(run)) {
    run <- get_current_run()
  }

  if (startsWith(run$id, "OfflineRun_")) {
    run$upload_files(
      name = names,
      paths = paths)
  } else {
    run$upload_files(
      names = names,
      paths = paths,
      timeout_seconds = timeout_seconds)
  }

  invisible(NULL)
}

print("R script run.")

args = commandArgs(trailingOnly=TRUE)
if (length(args) < 2) {
  stop(sprintf("Invalid arguments count, expect: 2, actual: %d.", length(args)))
}

status_file <- args[2]
error_msg <- ''
tryCatch(withCallingHandlers({
    print("Import packages.")
    check_and_import(list("reticulate", "jsonlite", "dplyr"))

    pd <- import("pandas")
    pa <- import("pyarrow")
    azureml <- import("azureml")

    decoded_params <- URLdecode(args[1])
    params <- fromJSON(decoded_params)
    input_paths <- params$input_paths
    input_schema_paths <- params$input_schema_paths
    output_paths <- params$output_paths
    output_schema_paths <- params$output_schema_paths
    custom_script <- params$custom_script

    print("R read input parquet file.")
    input_dataframe_1 <- load_dataframe_from_parquet(input_paths[1], input_schema_paths[1])
    input_dataframe_2 <- load_dataframe_from_parquet(input_paths[2], input_schema_paths[2])

    source(custom_script)

    if (!exists("azureml_main")) {
      stop("Could not find function \"azureml_main\".")
    }
    argument_list = formals(azureml_main)
    if (length(argument_list) == 0){
        warning("Invalid arguments count of function \"azureml_main\", expect: 2, actual: 0. Invoking azureml_main()...")
        results <- azureml_main()
    } else if (length(argument_list) == 1){
        warning("Invalid arguments count of function \"azureml_main\", expect: 2, actual: 1. Invoking azureml_main(input_dataframe_1)...")
        results <- azureml_main(input_dataframe_1)
    } else {
        results <- azureml_main(input_dataframe_1, input_dataframe_2)
    }

    if (!is.null(results)) {
      results <- convert_to_list(results)
      output_dataframe_1 <- results$dataset1
      output_dataframe_2 <- results$dataset2

      print("R generate output parquet file.")
      save_dataframe_to_parquet(output_dataframe_1, output_paths[1], output_schema_paths[1])
      save_dataframe_to_parquet(output_dataframe_2, output_paths[2], output_schema_paths[2])
    } else {
      warning("Empty result received from custom script.")
    }
  }, error = function(e) {
    # Remove the first three level stack traces due to they are meaningless.
    error_msg <<- paste(toString(e), toString(sys.calls()[-c(1:3)]), sep="\n")
    stop(e)
  }
), finally = {
  write(error_msg, status_file)
})

print("R script exit.")