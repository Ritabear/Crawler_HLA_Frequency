
import numpy as np
import matplotlib.pyplot as plt


class DrawBar:
    def __init__(self, labels, dataC, dataT):
        # 生成資訊
        self.labels = labels
        self.dataC = dataC
        self.dataT = dataT

    def drawDoubleBar(labels, dataC, dataT=[np.nan]):
        width = 0.4
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', 'r', 'b']
        xpos = np.arange(0, len(labels), 1)

        # 生成柱状圖
        fig, ax = plt.subplots(figsize=(10, 8))
        bars1 = plt.bar(xpos-width/2, dataC, align='center', width=width,
                        alpha=0.9, color='#1f77b4', label='China')
        bars2 = plt.bar(xpos+width/2, dataT, align='center', width=width,
                        alpha=0.9, color='#ff7f0e', label='Taiwan')
        # 設定每個柱子下面的記號
        fig.autofmt_xdate(rotation=45)
        ax.set_xticks(xpos)  # 確定每個記號的位置
        ax.set_xticklabels(labels)  # 確定每個記號的內容

        # 給每個柱子上面新增標註

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",  # 相對於被註釋點xy的偏移量（單位是點）
                            ha='center', va='bottom', size=5
                            )

        autolabel(bars1)
        autolabel(bars2)

        # 展示結果
        plt.legend()
        plt.show()
