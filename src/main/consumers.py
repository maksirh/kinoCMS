import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Ticket, Schedule


class BookingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.schedule_id = self.scope['url_route']['kwargs']['schedule_id']
        self.room_group_name = f'booking_{self.schedule_id}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        user = self.scope['user']

        if action == 'purchase_all':
            updated_tickets = await self.db_purchase_all_seats(user)
            for ticket in updated_tickets:
                await self.broadcast_status(ticket['row'], ticket['seat'], 'P')
            return


        row = data.get('row')
        seat = data.get('seat')

        if action == 'reserve':
            success = await self.db_reserve_seat(row, seat, user)
            if success:
                await self.broadcast_status(row, seat, 'R')

        elif action == 'cancel':
            success = await self.db_cancel_reservation(row, seat, user)
            if success:
                await self.broadcast_status(row, seat, 'free')

    @database_sync_to_async
    def db_reserve_seat(self, row, seat, user):
        if not Ticket.objects.filter(schedule_id=self.schedule_id, row=row, seat=seat).exclude(status='E').exists():
            Ticket.objects.create(
                schedule_id=self.schedule_id,
                row=row, seat=seat,
                user=user, status='R'
            )
            return True
        return False

    @database_sync_to_async
    def db_cancel_reservation(self, row, seat, user):
        ticket = Ticket.objects.filter(
            schedule_id=self.schedule_id,
            row=row, seat=seat,
            user=user, status='R'
        ).first()
        if ticket:
            ticket.delete()
            return True
        return False

    async def broadcast_status(self, row, seat, status):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'seat_update',
                'row': row,
                'seat': seat,
                'status': status
            }
        )

    async def seat_update(self, event):
        await self.send(text_data=json.dumps({
            'row': event['row'],
            'seat': event['seat'],
            'status': event['status']
        }))


    @database_sync_to_async
    def db_purchase_all_seats(self, user):
        tickets = Ticket.objects.filter(
            schedule_id=self.schedule_id,
            user=user,
            status='R'
        )
        updated_data = list(tickets.values('row', 'seat'))
        tickets.update(status='P')
        return updated_data