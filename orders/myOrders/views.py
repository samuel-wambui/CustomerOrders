from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .sms_utils import send_sms

from rest_framework import viewsets, status
from rest_framework.response import Response
from myOrders.models import Customer, Order
from myOrders.serializers import CustomerSerializer, OrderSerializer
from myOrders.sms_utils import send_sms  # Ensure correct import path for send_sms


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to send an SMS after creating an order.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        order = serializer.instance
        customer = order.customer

        # Send SMS to the customer
        message = (
            f"Dear {customer.name}, your order for {order.item} has been placed successfully. "
            f"Total: {order.amount:.2f}."
        )
        try:
            sms_response = send_sms(customer.phone_number, message)
            sms_status = sms_response["SMSMessageData"]["Recipients"][0]["status"]
        except Exception as e:
            sms_status = f"Failed: {e}"

        # Prepare and return the custom response
        response_data = {
            "message": f"Order for {order.item} created successfully.",
            "sms_status": sms_status,
            "data": serializer.data,
        }
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)



