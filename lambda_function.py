import json
import requests
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    # 날씨 정보 가져오기
    city = "Sasang"
    api_key = "27c09578263bf426599e99904828995e"
    weather_info = get_weather(city, api_key)

    # SMS 보내기
    send_sms(weather_info)

    return {
        'statusCode': 200,
        'body': json.dumps('SMS sent successfully!')
    }

def get_weather(city, api_key):
    lang = "kr"
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang={lang}"
    try:
        response = requests.get(api_url)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            current_temp = data["main"]["temp"]
            return {
                "city": city,
                "weather_description": weather_description,
                "current_temp": current_temp
            }
        else:
            return {"error": f"Failed to fetch weather data for {city}, status code: {response.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching weather data: {str(e)}"}

def send_sms(weather_info):
    # SMS 보내기 설정
    phone_number = '+8200000000000'
    message = f"{weather_info['city']}의 현재 날씨:\n\n날씨: {weather_info['weather_description']}\n현재 온도: {weather_info['current_temp']}도"

    try:
        response = sns.publish(
            PhoneNumber=phone_number,
            Message=message
        )
        print(f"{phone_number}로 SMS가 성공적으로 전송되었습니다. MessageId: {response['MessageId']}")
    except Exception as e:
        print(f"SMS 전송 실패: {e}")
