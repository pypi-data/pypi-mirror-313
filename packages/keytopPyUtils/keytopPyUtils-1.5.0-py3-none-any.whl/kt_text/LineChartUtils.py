import ast

from matplotlib import pyplot as plt

from kt_base import CommonUtils
from kt_text.Config import Config


class LineChartUtils:
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
        # 构建字符串表示
        field_str = ', '.join([f"{k}={v}" for k, v in fields.items()])
        return f"LineChartUtils({field_str})"

    def generate_line_chart(self):
        """
        生成折线图
        :return: 返回文件名称
        """
        x = []
        # 初始化一个字典来存储每个键对应的所有值
        grouped_data = {key: [] for key in self.y_keys}

        # 遍历 data 列表，按 y_keys 中的每个键分组取值
        for item in self.data:
            x.append(item.get(self.x_key))
            for key in self.y_keys:
                grouped_data[key].append(item[key])

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimSun']  # 使用微软雅黑
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        # 创建图表和坐标轴
        fig, ax = plt.subplots(figsize=(10, 6), dpi=500)

        # 设置图表背景色
        fig.patch.set_facecolor('#FFFFFF')  # 设置整个图表的背景色
        fig.subplots_adjust(left=0.1)  # 设置左侧距离为画布宽度的 10%
        fig.subplots_adjust(bottom=0.2)
        ax.set_facecolor('#FFFFFF')  # 设置坐标轴区域的背景色
        # 设置图表边框颜色
        for spine in ax.spines.values():
            spine.set_color('#d7d7d7')  # 将所有边框颜色设置为红色
        # 绘制折线图，并设置线条颜色
        for key in self.y_keys:
            ax.plot(x, grouped_data[key], label=key, color=self.y_keys[key], marker='o', linestyle='-')

        # 设置横坐标和纵坐标上的文字大小
        ax.tick_params(axis='x', labelsize=12)  # 设置 X 轴刻度标签的文字大小
        ax.tick_params(axis='y', labelsize=12)  # 设置 Y 轴刻度标签的文字大小
        # ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=12, frameon=False)

        # 添加图例，并设置图例的位置和样式
        legend = ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=8,
                           frameon=False, handlelength=1, handletextpad=0.6, fontsize=10)

        # 调整图表与画布边缘的距离
        fig.subplots_adjust(bottom=0.25)  # 增加底部距离，以容纳图例

        # 添加标题和标签
        ax.set_title(self.title_name, color=self.title_color, fontsize=self.title_font_size, fontweight='bold', pad=15)  # 设置标题颜色
        ax.set_xlabel(self.x_label_name, color=self.x_label_color, fontsize=14, labelpad=10)  # 设置X轴标签颜色
        ax.set_ylabel(self.y_label_name, color=self.y_label_color, fontsize=14, labelpad=10)  # 设置Y轴标签颜色

        # 设置刻度颜色
        ax.tick_params(colors='#333333')

        # 显示网格
        ax.grid(True, linestyle='--', color='#D3D3D3')

        file_name = CommonUtils.generate_uuid() + ".png";
        # 保存图表为PNG文件
        plt.savefig(Config.BASE_PATH+file_name)
        return file_name

