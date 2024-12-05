from collections import namedtuple

import pandas as pd

TprFprPair = namedtuple("TprFprPair", "tpr fpr")


class ReportNameConstants:
    ScoredDataReportName = 'scoredData'
    ToComparedDataReportName = 'scoredDataToCompare'


class ScoreBin:
    def __init__(self, bin_start, bin_end, true_positive=0, true_negative=0, false_positive=0, false_negative=0,
                 num_positive=0, num_negative=0, count=0, auc=0):
        self.bin_start = bin_start
        self.bin_end = bin_end
        self.true_positive = true_positive
        self.true_negative = true_negative
        self.num_positive = num_positive
        self.num_negative = num_negative
        self.false_positive = false_positive
        self.false_negative = false_negative
        self.count = count
        self.auc = auc

    def set_statistic(self, true_sample_number, counts):
        self.num_positive = true_sample_number
        self.count = counts
        self.num_negative = counts - true_sample_number

    @property
    def f1(self):
        sum_pre_recall = self.precision + self.recall
        return 0.0 if (abs(sum_pre_recall) < 1e-9) else 2.0 * self.precision * self.recall / sum_pre_recall

    @property
    def recall(self):
        truth_positive = self.true_positive + self.false_negative
        return 0 if truth_positive == 0 else self.true_positive / truth_positive

    @property
    def precision(self):
        predict_positive = self.true_positive + self.false_positive
        return 1.0 if predict_positive == 0 else self.true_positive / predict_positive

    @property
    def neg_recall(self):
        truth_negative = self.true_negative + self.false_positive
        return 1.0 if truth_negative == 0 else self.true_negative / truth_negative

    @property
    def neg_precision(self):
        predict_negative = self.true_negative + self.false_negative
        return 1.0 if predict_negative == 0 else self.true_negative / predict_negative

    @property
    def accuracy(self):
        instance_num = self.true_negative + self.true_positive + self.false_positive + self.false_negative
        return 0.0 if instance_num == 0 else (self.true_positive + self.true_negative) / instance_num

    @property
    def tpr(self):
        """
        calculate True Positive Rate (tpr), defined as : true positive / total positive instance
        :return:
        """
        p = self.true_positive + self.false_negative
        return 0.0 if p == 0 else self.true_positive / p

    @property
    def fpr(self):
        """
        calculate False Positive Rate (fpr), defined as : false positive / total negative instance
        """
        n = self.false_positive + self.true_negative
        return 0.0 if n == 0 else self.false_positive / n

    @property
    def y_rate(self):
        """
        calculate y_rate to draw LIFT curve.
        y_rate is defined as: Predictive Positive Rate = predict pos / total
        :return:
        """
        instance_num = self.true_negative + self.true_positive + self.false_positive + self.false_negative
        predicted_positives = self.true_positive + self.false_positive
        return 0.0 if instance_num == 0 else predicted_positives / instance_num

    def finalize(self, prev_bin, total_positives, total_negatives):
        self.true_positive = self.num_positive
        self.false_positive = self.num_negative
        if prev_bin is not None:
            self.true_positive += prev_bin.true_positive
            self.false_positive += prev_bin.false_positive

        self.false_negative = total_positives - self.true_positive
        self.true_negative = total_negatives - self.false_positive


class ScoreBinner:
    def __init__(self, num_buckets):

        self.num_buckets = num_buckets
        self.min_score = 0.0
        self.max_score = 1.0
        self.total_positive = 0
        self.total_negative = 0
        self.bins = [None] * (self.num_buckets + 1)
        self.tpr_fpr_pairs = [None] * self.num_buckets
        self.gap = (self.max_score - self.min_score) / self.num_buckets

    def _calculate_bin_index_by_prob(self, probability):
        if abs(probability - self.max_score) < 1e-9:
            bin_index = self.num_buckets - 1
        else:
            bin_index = int((probability - self.min_score) / self.gap)
        return bin_index

    def build_chart(self, df, prob_column_name, label_column_name):
        if df.shape[0] == 0:
            return [ScoreBin(self.min_score, self.max_score)]

        bin_start = self.min_score
        # initialize buckets
        for i in range(self.num_buckets):
            self.bins[i] = ScoreBin(bin_start, bin_start + self.gap)
            bin_start += self.gap

        # assign instance to bins by probability
        df['bin_index'] = df[prob_column_name].apply(
            lambda x: self._calculate_bin_index_by_prob(x))

        # count total positive and negative ground-truth
        self.total_positive = df[df[label_column_name] > 0.5].shape[0]
        self.total_negative = df.shape[0] - self.total_positive
        # count each bin
        counts_df = df.groupby(by='bin_index', as_index=False).agg(
            {label_column_name: 'sum', prob_column_name: 'count'})
        counts_df.rename(inplace=True,
                         columns={label_column_name: 'num_positive',
                                  prob_column_name: 'bin_counts'})
        counts_df['num_positive'] = counts_df['num_positive'].apply(lambda x: round(x, 0))
        # add threshold = 1.0 manually.
        self.bins[self.num_buckets] = ScoreBin(bin_start=1.0, bin_end=1.0, false_negative=self.total_positive,
                                               true_negative=self.total_negative)
        # update statistic information in each bin
        for index, row in counts_df.iterrows():
            bin_index = int(row['bin_index'])
            num_positive = int(row['num_positive'])
            bin_counts = int(row['bin_counts'])
            self.bins[bin_index].set_statistic(num_positive, bin_counts)
        prev_bin = None
        loop_range = range(0, self.num_buckets)
        for i in loop_range[::-1]:  # loop from last one to first one
            self.bins[i].finalize(prev_bin, self.total_positive, self.total_negative)
            prev_bin = self.bins[i]
            self.tpr_fpr_pairs[i] = TprFprPair(tpr=self.bins[i].tpr, fpr=self.bins[i].fpr)

    def compress_bins(self, out_compressed_bins_num):
        bins_per_partition = int(self.num_buckets / out_compressed_bins_num)
        out_bins = [None] * out_compressed_bins_num
        end_threshold = self.bins[self.num_buckets - 1].bin_end
        prev_auc = 0.0

        current_coarse_bin_index = out_compressed_bins_num - 1
        fine_bin_count = 0
        bin_instances = 0
        positive_cumulative = 0
        negative_cumulative = 0
        end_index = self.num_buckets - 1

        loop_range = range(0, self.num_buckets)
        for i in loop_range[::-1]:
            start_threshold = self.bins[i].bin_start
            bin_instances += self.bins[i].count
            positive_cumulative += self.bins[i].num_positive
            negative_cumulative += self.bins[i].num_negative
            fine_bin_count += 1
            if fine_bin_count == bins_per_partition:
                tp = self.bins[i].true_positive
                fp = self.bins[i].false_positive
                fn = self.total_positive - tp
                tn = self.total_negative - fp
                auc = prev_auc + self._compute_auc(i, end_index)
                out_bin = ScoreBin(bin_start=start_threshold, bin_end=end_threshold, true_positive=tp,
                                   true_negative=tn, false_positive=fp, false_negative=fn,
                                   num_positive=positive_cumulative, num_negative=negative_cumulative,
                                   count=bin_instances, auc=auc)
                out_bins[current_coarse_bin_index] = out_bin
                current_coarse_bin_index -= 1
                prev_auc = auc
                fine_bin_count = 0
                end_index = i
                end_threshold = start_threshold
                bin_instances = 0
                positive_cumulative = 0
                negative_cumulative = 0
        return out_bins

    def _compute_auc(self, start_index, end_index):
        if end_index <= start_index:
            return 0
        left_fpr = self.tpr_fpr_pairs[start_index].fpr
        left_height = self.tpr_fpr_pairs[start_index].tpr
        cumulative_area = 0.0

        for i in range(start_index, end_index):
            index = i + 1
            right_fpr = self.tpr_fpr_pairs[index].fpr
            delta_x = left_fpr - right_fpr
            right_height = self.tpr_fpr_pairs[index].tpr
            average_height = (left_height + right_height) / 2.0
            cumulative_area += delta_x * average_height
            left_fpr = right_fpr
            left_height = right_height
        return cumulative_area

    def get_chart(self):
        chart_list = []
        for single_bin in self.bins:
            item_list = single_bin.get_variable_values()
            chart_list.append(item_list)
        return pd.DataFrame(chart_list, columns=self.bins[0].get_variable_names())


class ChartData:
    def __init__(self, coarse_data, data_points, auc, min_value, max_value, positive_label=None, negative_label=None):
        self.coarse_data = coarse_data
        self.data_points = data_points
        self.auc = auc
        self.min_value = min_value
        self.max_value = max_value
        self.positive_label = str(positive_label)
        self.negative_label = str(negative_label)


class ReportData:
    def __init__(self, df, prob_column_name, label_column_name, report_name: str, positive_label: str,
                 negative_label: str, num_bins: int = 10, auc=None):
        """
        Report Data contained all information which will be visualized.
        azureml/studio/common/jsonconverter/report_data_json_converter.py will be used to convert this class to json.
        :param df: pandas.DataFrame. Scored Data Frame
        :param prob_column_name: The name of probability column
        :param label_column_name: The name of label column
        :param report_name: The name of the report
        :param num_bins: The number of bins to construct for evaluation metrics
        """

        self.report_name = report_name
        self.num_buckets = 1000  # Same precision as Studio v1
        binner = ScoreBinner(num_buckets=self.num_buckets)
        binner.build_chart(df, prob_column_name, label_column_name=label_column_name)
        if df.shape[0] == 0:
            self.chart = ChartData(coarse_data=[], data_points=[], auc=None, min_value=binner.min_score,
                                   max_value=binner.max_score, positive_label=positive_label,
                                   negative_label=negative_label)
        else:
            self.chart = ChartData(coarse_data=binner.compress_bins(num_bins), data_points=binner.bins, auc=auc,
                                   min_value=binner.min_score, max_value=binner.max_score,
                                   positive_label=positive_label,
                                   negative_label=negative_label)
