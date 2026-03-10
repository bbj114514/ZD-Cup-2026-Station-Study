import pandas as pd
import jieba
import jieba.analyse
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def get_high_contrast_cmap(base_cmap_name, start_frac=0.4):
    base_cmap = plt.get_cmap(base_cmap_name)
    colors = base_cmap(np.linspace(start_frac, 1.0, 256))
    return mcolors.LinearSegmentedColormap.from_list(f"{base_cmap_name}_hc", colors)

def generate_shaped_wordcloud(text_col, mask_path, base_cmap, start_frac, save_name, title):
    text_list = df_open[text_col].replace(['-', '.', '无', '暂无', '。'], pd.NA).dropna()
    full_text = " ".join(text_list)

    for word in ['充电桩', '电动车', '消防设施', '休息区', '外卖骑手', '快递员']:
        jieba.add_word(word)

    STOPWORDS = {
        "希望", "建议", "觉得", "可以", "但是", "看到", "比较", "我们", "支持", "建设",
        "一个", "有个", "这种", "他们", "你们", "它是", "一点", "一些", "必须", "一定",
        "需要", "应该", "能建", "非常", "特别", "地方", "事情", "东西", "情况", "问题",
        "已经", "这样", "由于", "只是", "还是", "甚至", "而且", "还有", "为了", "因为",
        # 过于通用、遮盖实质信息的词
        "想法", "意见", "知道", "没有", "遇到", "大家", "没", "有", "的", "了",
        "就是", "感觉", "不是", "这个", "那个", "进行", "提供", "发现", "认为",
    }

    keywords_dict = jieba.analyse.extract_tags(
        full_text,
        topK=200,
        withWeight=True,
        allowPOS=('n', 'vn', 'v')
    )

    filtered_freqs = {w: f for w, f in keywords_dict if w not in STOPWORDS and len(w) > 1}

    if not filtered_freqs:
        print(f"[警告] {text_col} 过滤后无关键词，跳过。")
        return

    try:
        mask_image = np.array(Image.open(mask_path))
    except FileNotFoundError:
        print(f"[警告] 遮罩文件未找到: {mask_path}，跳过。")
        return

    hc_cmap = get_high_contrast_cmap(base_cmap, start_frac)

    wc = WordCloud(
        font_path='simhei.ttf',
        background_color='white',
        mask=mask_image,
        contour_width=2,
        contour_color='steelblue',
        width=1200, height=1000,
        colormap=hc_cmap,
        max_words=35,
        max_font_size=150,
        min_font_size=16,
        prefer_horizontal=0.85,
        relative_scaling=0.8,
        random_state=42
    ).generate_from_frequencies(filtered_freqs)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wc, interpolation='bilinear')
    ax.set_title(title, fontsize=20, pad=20)
    ax.axis("off")
    plt.tight_layout()
    save_path = os.path.join(base_dir, save_name)
    fig.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"已保存: {save_path}")

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'open_data.csv')
rider_path = os.path.join(base_dir, 'rider.png')
merchant_path = os.path.join(base_dir, 'merchant.png')
resident_path = os.path.join(base_dir, 'resident.png')

df_open = pd.read_csv(csv_path, encoding='utf-8')

generate_shaped_wordcloud('Q23_运营顾虑_开放',   rider_path,    'Oranges', 0.4, 'shaped_rider_wc.png',    'WordCloud: Rider Concerns')
generate_shaped_wordcloud('Q33_商户具体想法_开放', merchant_path, 'Blues',   0.4, 'shaped_merchant_wc.png', 'WordCloud: Merchant Ideas')
generate_shaped_wordcloud('Q41_居民建议建议_开放', resident_path, 'Greys',   0.5, 'shaped_resident_wc.png',  'WordCloud: Resident Suggestions')