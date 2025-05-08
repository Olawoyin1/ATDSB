import requests
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactUsSerializer

class ContactUsView(APIView):
    def post(self, request):
        # Use the serializer to validate the data
        serializer = ContactUsSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data  # Validated data from the form
            

            formatted_message = data["message"].replace("\n", "<br>")
            sender_name = data["name"]
            sender_email = data["email"]
            message = data["message"]
            
            # Setup the email payload
            payload = {
                "sender": {
                    "name": "ATDS Website Contact",  # Sender name (you can change this)
                    "email": config("DEFAULT_FROM_EMAIL")  # Sender email from .env
                },
                "to": [
                    {
                        "email": config("NOTIFY_EMAIL"),  # The office email that will get the message
                        "name": "ATDS"
                    }
                ],
                "subject": "New Contact Message from ATDS Website📩",  # Subject of the email
                "htmlContent": f"""
                    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; border-radius: 5px;">
                        <h2 style="color: #333;">New Contact Message</h2>
                        <p style="font-size: 16px; color: #555;">You have received a new message from your website contact form:</p>
                        <div style="background-color: #fff; border: 1px solid #ddd; padding: 20px; border-radius: 5px;">
                            <p><strong style="color: #333;">Name:</strong> {sender_name}</p>
                            <p><strong style="color: #333;">Email:</strong> {sender_email}</p>
                            <p><strong style="color: #333;">Message:</strong></p>
                            <div style="background-color: #f1f1f1; border: 1px solid #ddd; padding: 18px; margin-top: 10px;">
                                {message}
                            </div>
                        </div>
                        <p style="margin-top: 20px; font-size: 14px; color: #999;">This message was sent via the website contact form.</p>
                    </div>
                """
            }

            # Set up headers with your Brevo API key
            headers = {
                "accept": "application/json",
                "api-key": config("BREVO_API_KEY"),
                "content-type": "application/json"
            }

            # Send the email through Brevo
            try:
                response = requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    json=payload,
                    headers=headers
                )

                if response.status_code == 201:
                    # Successfully sent email
                    return Response({"message": "Message sent successfully."}, status=status.HTTP_200_OK)
                else:
                    # Failed to send email
                    return Response({
                        "error": "Failed to send email.",
                        "details": response.json()
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # If data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
