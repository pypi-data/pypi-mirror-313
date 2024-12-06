import ast

from matplotlib import pyplot as plt
from kt_base import CommonUtils
from kt_text.Config import Config


class ChartGenerator:
    def __init__(self,param):
        self.title_name = param.get("titleName")
        if self.title_name is None:
            self.title_name = ""
        self.title_color = param.get("titleColor")
        if self.title_color is None or not self.title_color.startswith('#'):
            self.title_color = "#EE3B3B"
        self.title_font_size = param.get("titleFontSize")
        if self.title_font_size is None:
            self.title_font_size = 16

        self.x_label_name = param.get("xLabelName")
        if self.x_label_name is None:
            self.x_label_name = "X轴"
        self.x_label_color = param.get("xLabelColor")
        if self.x_label_color is None or not self.x_label_color.startswith('#'):
            self.x_label_color = "#333333"

        self.y_label_name = param.get("yLabelName")
        if self.y_label_name is None:
            self.y_label_name = "Y轴"
        self.y_label_color = param.get("yLabelColor")
        if self.y_label_color is None or not self.y_label_color.startswith('#'):
            self.y_label_color = "#333333"

        self.x_key = param.get("xKey")
        if self.x_key is None:
            raise Exception("X轴取数标识：xKey，不能为空")

        self.y_keys = param.get("yKeys")
        if self.y_keys is None:
            raise Exception("Y轴取数标识：yKeys，不能为空")
        self.y_keys = ast.literal_eval("{" + self.y_keys + "}")

        self.data = param.get("data")
        if self.data is None:
            raise Exception("用于生成折线图的数据：data，不能为空")
        if isinstance(self.data, str):
            self.data = ast.literal_eval(self.data)

    def __str__(self):
        fields = vars(self)
        field_str = ', '.join([f"{k}={v}" for k, v in fields.items()])
        return f"LineChartUtils({field_str})"

    def generate_line_chart(self):
        """
        生成折线图
        :return: 返回文件名称
        """
        grouped_data, x = self.build_data()
        ax = self.before_config()
        for key in self.y_keys:
            ax.plot(x, grouped_data[key], label=key, color=self.y_keys[key], marker='o', linestyle='-')

        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        self.legend_config(ax)
        return self.save_img()



    def generate_bar_chart(self):
        """
        生成柱状图
        :return: 返回文件名称
        """
        grouped_data, x = self.build_data()
        ax = self.before_config()

        bar_width = 0.2
        min_bar_width = 0.05
        team_size = len(grouped_data)
        if team_size > 2:
            bar_width = bar_width - (team_size - 2) * 0.02
        if bar_width < min_bar_width:
            bar_width = min_bar_width
        index = range(len(x))

        def draw_bars(ax, index, sales_data, width):
            bars = []
            for i, (team, sales) in enumerate(sales_data.items()):
                offset = width * i - (width * (len(sales_data) - 1)) / 2
                bars.append(ax.bar([x + offset for x in index], sales, width, color=self.y_keys[team], label=team, zorder=2))
            return bars

        bars = draw_bars(ax, index, grouped_data, bar_width)
        ax.set_xticks([i for i in index])
        ax.set_xticklabels(x)

        self.legend_config(ax)

        def add_labels(bars):
            for bar_set in bars:
                for rect in bar_set:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

        add_labels(bars)
        return self.save_img()

    def legend_config(self, ax):
        ax.legend(loc='lower center', bbox_to_anchor=(0.5,-0.22), ncol=8,
                  frameon=False, handlelength=1, handletextpad=0.6, fontsize=10)
        ax.tick_params(colors='#333333')
        ax.grid(True, linestyle='--', color='#D3D3D3', zorder=1)

    def save_img(self):
        file_name = CommonUtils.generate_uuid() + ".png";
        plt.savefig(Config.BASE_PATH + file_name)
        return file_name

    def before_config(self):
        plt.rcParams['font.sans-serif'] = ['SimSun']
        plt.rcParams['axes.unicode_minus'] = False
        fig, ax = plt.subplots(figsize=(10, 6), dpi=500)
        fig.patch.set_facecolor('#FFFFFF')
        fig.subplots_adjust(left=0.1)
        fig.subplots_adjust(bottom=0.2)
        ax.set_facecolor('#FFFFFF')
        for spine in ax.spines.values():
            spine.set_color('#d7d7d7')
        #
        ax.set_title(self.title_name, color=self.title_color, fontsize=self.title_font_size, fontweight='bold',
                     pad=20)
        ax.set_xlabel(self.x_label_name, color=self.x_label_color, fontsize=14, labelpad=10)
        ax.set_ylabel(self.y_label_name, color=self.y_label_color, fontsize=14, labelpad=10)
        return ax

    def build_data(self):
        x = []
        grouped_data = {key: [] for key in self.y_keys}
        for item in self.data:
            x.append(item.get(self.x_key))
            for key in self.y_keys:
                grouped_data[key].append(item[key])
        return grouped_data, x
