import requests

# URL API
BASE_URL = "http://localhost:5000/api/statistics"


# Функция для получения статистики
def get_statistics():
    response = requests.get(f"{BASE_URL}/get")
    if response.status_code == 200:
        statistics = response.json()
        print("Statistics retrieved successfully:")
        for stat in statistics:
            print(f"Time: {stat['time']}, Accuracy: {stat['accuracy']}%, WPM: {stat['wpm']}")
    else:
        print(f"Failed to retrieve statistics: {response.text}")

# Пример получения статистики
get_statistics()
