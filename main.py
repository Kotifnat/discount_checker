from apscheduler.schedulers.background import BackgroundScheduler
import requests

from bot_interface import listen, nl, session


scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=10)
def check():
    users = [125159825]
    list_of_discount_products = []
    with open('list_of_products.txt', 'r') as f:
        for link in f:
            link = link.rstrip('\n')
            response =  requests.get(link)
            discount = response.content.find(b'abs_discount')
            if discount >=0:
                list_of_discount_products.append(link)
    session.method('messages.send', {'user_ids':users, 'message': f'{nl.join(list_of_discount_products)} - беги скорее покупай', 'random_id': 0})

if __name__ == '__main__':
    scheduler.start()
    listen()