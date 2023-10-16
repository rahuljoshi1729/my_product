from drf_yasg import openapi

api_info = openapi.Info(
    title="E_commerce portal",
    default_version='v1',
    description="API description",
    terms_of_service="https://www.yourapi.com/terms/",
    contact=openapi.Contact(email="contact@yourapi.com"),
    license=openapi.License(name="Your License"),
)