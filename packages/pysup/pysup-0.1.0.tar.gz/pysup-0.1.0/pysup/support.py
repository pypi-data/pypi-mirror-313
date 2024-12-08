#!/usr/bin/env python3
# coding: utf-8

from asyncio import run as asyncio_run
from httpx import AsyncClient
from enum import Enum
from decouple import config


class Ticket:
    class RequestMethod(Enum):
        GET = 1
        POST = 2
        DELETE = 3
        PATCH = 4
        PUT = 5

    def __init__(self, *, base_url: str | None = None, secret_token: str | None = None):
        self.BASE_URL = base_url or config("SUPPORT_BASE_URL")
        self.HEADER = {
            "Authorization": secret_token or f"Bearer {config("SUPPORT_SECRET_TOKEN")}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # Make the Request Methods
    async def get(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.get(url=url, headers=self.HEADER, params=data)
            response.raise_for_status()
            return response.json()

    async def post(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.post(url=url, headers=self.HEADER, json=data)
            response.raise_for_status()
            return response.json()

    async def put(self, url: str, data: dict | None = None) -> dict:
        async with AsyncClient() as client:
            response = await client.put(url=url, headers=self.HEADER, json=data)
            response.raise_for_status()
            return response.json()

    async def delete(self, url: str) -> dict:
        async with AsyncClient() as client:
            response = await client.delete(url=url, headers=self.HEADER)
            response.raise_for_status()
            return response.json()

    async def request(self, url: str, method: int, data: dict | None = None) -> dict | None:
        match method:
            case Ticket.RequestMethod.GET.value:
                return await self.get(url, data)

            case Ticket.RequestMethod.POST.value:
                return await self.post(url, data)

            case Ticket.RequestMethod.PUT.value:
                return await self.put(url, data)

            case Ticket.RequestMethod.DELETE.value:
                return await self.delete(url)

    # Log
    async def log_list_async(self, log_id: int | str) -> dict | None:
        log_id = str(log_id) if isinstance(log_id, int) else log_id

        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/getLog/{log_id}",
        )

    def log_list_sync(self, log_id: int | str) -> dict | None:
        return asyncio_run(self.log_list_async(log_id=log_id))

    # Department
    async def department_list_async(self) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/department",
        )

    def department_list_sync(self) -> dict | None:
        return asyncio_run(self.department_list_async())

    async def department_create_async(self, *, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.POST.value,
            url=f"{self.BASE_URL}/department",
            data=data,
        )

    def department_create_sync(self, *, data: dict) -> dict | None:
        return asyncio_run(self.department_create_async(data=data))

    async def department_get_async(self, *, department_id: int) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/department/{department_id}",
        )

    def department_get_sync(self, *, department_id: int) -> dict | None:
        return asyncio_run(self.department_get_async(department_id=department_id))

    async def department_update_async(self, *, department_id: int, data: dict, delete: bool) -> dict | None:
        if delete:
            return await self.request(
                method=Ticket.RequestMethod.DELETE.value,
                url=f"{self.BASE_URL}/department/{department_id}",
            )
        else:
            return await self.request(
                method=Ticket.RequestMethod.PUT.value,
                url=f"{self.BASE_URL}/department/{department_id}",
                data=data,
            )

    def department_update_sync(self, *, department_id: int, data: dict, delete: bool) -> dict | None:
        return asyncio_run(self.department_update_async(department_id=department_id, data=data, delete=delete))

    # Ticket
    async def ticket_list_async(self, ticket_id: int | str | None) -> dict | None:
        if ticket_id:
            ticket_id = str(ticket_id) if isinstance(ticket_id, int) else ticket_id
            url = f"{self.BASE_URL}/ticket/{ticket_id}"
        else:
            url = f"{self.BASE_URL}/ticket"

        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=url,
        )

    def ticket_list_sync(self, ticket_id: int | str | None) -> dict | None:
        return asyncio_run(self.ticket_list_async(ticket_id=ticket_id))

    async def ticket_replies_async(self, ticket_id: int | str) -> dict | None:
        ticket_id = str(ticket_id) if isinstance(ticket_id, int) else ticket_id

        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket/{ticket_id}/replies",
        )

    def ticket_replies_sync(self, ticket_id: int | str) -> dict | None:
        return asyncio_run(self.ticket_replies_async(ticket_id=ticket_id))

    async def ticket_update_async(self, *, ticket_id: int, data: dict, delete: bool) -> dict | None:
        if delete:
            return await self.request(
                method=Ticket.RequestMethod.DELETE.value,
                url=f"{self.BASE_URL}/ticket/{ticket_id}",
            )
        else:
            return await self.request(
                method=Ticket.RequestMethod.PUT.value,
                url=f"{self.BASE_URL}/ticket/{ticket_id}",
                data=data,
            )

    def ticket_update_sync(self, *, ticket_id: int, data: dict, delete: bool) -> dict | None:
        return asyncio_run(self.ticket_update_async(ticket_id=ticket_id, data=data, delete=delete))

    async def ticket_attach_async(self, file_id: int | str) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/file/{file_id}",
        )

    def ticket_attach_sync(self, file_id: int | str) -> dict | None:
        return asyncio_run(self.ticket_attach_async(file_id=file_id))

    # Replies
    async def replies_create_async(self, *, data: dict) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.POST.value,
            url=f"{self.BASE_URL}/ticket-replies",
            data=data,
        )

    def replies_create_sync(self, *, data: dict) -> dict | None:
        return asyncio_run(self.ticket_replies_create_async(data=data))

    async def replies_update_async(self, *, reply_id: int, data: dict, delete: bool) -> dict | None:
        if delete:
            return await self.request(
                method=Ticket.RequestMethod.DELETE.value,
                url=f"{self.BASE_URL}/ticket-replies/{reply_id}",
            )
        else:
            return await self.request(
                method=Ticket.RequestMethod.PUT.value,
                url=f"{self.BASE_URL}/ticket-replies/{reply_id}",
                data=data,
            )

    def replies_update_sync(self, *, reply_id: int, data: dict, delete: bool) -> dict | None:
        return asyncio_run(self.replies_update_async(reply_id=reply_id, data=data, delete=delete))

    async def replies_get_async(self, *, reply_id: int) -> dict | None:
        return await self.request(
            method=Ticket.RequestMethod.GET.value,
            url=f"{self.BASE_URL}/ticket-replies/{reply_id}",
        )

    def replies_get_sync(self, *, reply_id: int) -> dict | None:
        return asyncio_run(self.replies_get_async(reply_id=reply_id))
