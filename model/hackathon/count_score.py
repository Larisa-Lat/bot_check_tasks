import pandas as pd
import sklearn.metrics
import logging
logger = logging.getLogger("main_logger.count_score")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


async def count_score(values, case, path_to_preds_file):
    """
    values = таблица с правильными ответами
    case - инфа об необходимом кейсе
    path_to_preds_file - csv файл с двумя колонками: id, pred_value
    
    Возвращет 
    Если все хорошо - float число(скор)
    Или "error" - в случае когда отпарвлен не тот файл
    """

    # Перевод данных в Dataframe
    df = pd.DataFrame(values).set_index("id")
    # Считать данные пользователя
    df_pred = pd.read_csv(path_to_preds_file, index_col="id")

    # Присоеденить к датафрейму по айди
    df = df.join(df_pred, how="left")
    # Проверить ту ли таблицу прислали
    is_secuence_ok = sorted(list(df.index.values)) == sorted(list(df_pred.index.values))

    if not is_secuence_ok:
        return "error"

    # Расчитиатть и вернуть метрику
    metric_function = getattr(sklearn.metrics, case["metric_func"])
    metric = metric_function(df["true_value"], df["pred_value"])

    return metric













