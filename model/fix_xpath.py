import time

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By


def find_element(url):

    options = webdriver.ChromeOptions()
    options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=options)

    browser.get(url)
    time.sleep(1)
    data = browser.find_element(By.XPATH, "//div[text()='Public Score']/following-sibling::p")
    return data.text


if __name__ == "__main__":
    urls = ["https://www.kaggle.com/code/raulmois05/sherlock-cata-and-watson-raul-on-the-case",
            "https://www.kaggle.com/code/ruchikarani/contradictory-my-dear-watson-prediction",
            "https://www.kaggle.com/code/shadesh/my-dear-watson-lstm-model",
            "https://www.kaggle.com/code/raulmois05/sherlock-cata-and-watson-raul-on-the-case",
            "https://www.kaggle.com/code/xyznihal/random-forest-algorithm-for-my-dear-watson",
            "https://www.kaggle.com/code/jamessuryaputra/wrecking-text-deaf",
            "https://www.kaggle.com/code/vempaliakhil96/03-exp-inf",
            "https://www.kaggle.com/code/vempaliakhil96/exp-2",
            "https://www.kaggle.com/code/yeejian/petals-to-the-metal-resnet",
            "https://www.kaggle.com/code/shadesh/just-fun",
            "https://www.kaggle.com/code/nadiahamane/detecting-contradiction-and-entailment-in-multilin",
            "https://www.kaggle.com/code/ssravipati/contradictory-bert",
            "https://www.kaggle.com/code/wrebelz/contradiction",
            "https://www.kaggle.com/code/mukesharipaka/contradictory-bert",
            "https://www.kaggle.com/code/yashpuri1912/my-dear-watson",
            "https://www.kaggle.com/code/atamazian/fc-swin-large-with-external-data",
            "https://www.kaggle.com/code/antoniozs/swinlarge-plus-external-data",
            "https://www.kaggle.com/code/heshamzaky/final",
            "https://www.kaggle.com/code/larjeck/flower-classification-with-accelerator",
            "https://www.kaggle.com/code/rafaaalalwani/project-swin-b",
            "https://www.kaggle.com/code/dmitrynokhrin/start-with-ensemble-v2",
            "https://www.kaggle.com/code/hayko1995/fc-ensemble-external-data-effnet-densenet",
            "https://www.kaggle.com/code/luongduongminh/effnet-densenet",
            "https://www.kaggle.com/code/ahmedmurad1990/fc-ensemble-external-data-2",
            "https://www.kaggle.com/code/acepheus/petals-to-the-metal-predict",
            "https://www.kaggle.com/code/acepheus/petals-to-the-metal-predict",
            "https://www.kaggle.com/code/dmitrynokhrin/densenet201-aug-additional-data",
            "https://www.kaggle.com/code/maso0dahmed/predicting-different-types-of-flowers",
            "https://www.kaggle.com/code/pritamkumarmehta/notebook6d98a9823b",
            "https://www.kaggle.com/code/akashsuper2000/flower-classification-with-tpus",
            "https://www.kaggle.com/code/dmitrynokhrin/xception-aug-additional-data",
            "https://www.kaggle.com/code/georgezoto/computer-vision-petals-to-the-metal",
            "https://www.kaggle.com/code/leoisleo1/fork-of-flower-classification-with-tpus",
            "https://www.kaggle.com/code/bhargavrko619/notebook",
            "https://www.kaggle.com/code/syedjarullahhisham/ptom-extdata-effnet-densenet-xceptnet-ensemble",
            "https://www.kaggle.com/code/andyden/flowers-with-keras",
            "https://www.kaggle.com/code/biene94/flower-classification",
            "https://www.kaggle.com/code/gustavomsilva/flower-classification-computer-vision-using-tpu",
            "https://www.kaggle.com/code/omarkhd99/flowers",
            "https://www.kaggle.com/code/akataev96/start-with-pre-train-0895d8",
            "https://www.kaggle.com/code/lkatran/start-with-ensemble-v3",
            "https://www.kaggle.com/code/nachiket273/pytorch-tpu-vision-transformer",
            "https://www.kaggle.com/code/tuckerarrants/kfold-efficientnet-augmentation-s",
            "https://www.kaggle.com/code/nileshsuthar/petal-to-the-metals-all-cnn-models",
            "https://www.kaggle.com/code/hughzzw/flower-efficientnetb7-densenet201-0-96",
            "https://www.kaggle.com/code/fayzerr/flower-classification-on-tpu-using-cnn-models",
            "https://www.kaggle.com/code/ging21/petals",
            "https://www.kaggle.com/code/atamazian/flower-classification-ensemble-effnet-densenet",
            "https://www.kaggle.com/code/amartyamukherjee/efficientnet-v2-xl-flower-classification",
            "https://www.kaggle.com/code/gregmadden/flowers-grm7q2"
            ]

    count_ans = 0
    for url in urls:
        ans = find_element(url)
        count_ans += 1
        print(count_ans)

    print("great") if count_ans == len(urls) else print("problems")