from django.http import JsonResponse
from django.utils.translation import (
    gettext_lazy as _,
)
from postcodes.settings import (
    REQUIRES_AUTH,
)
from postcodes.postcode import (
    address_check,
    AddressValidationError,
    logger,
)

def address_check_api(request):
    # Check if the user is authenticated (if required)
    if REQUIRES_AUTH and not request.user.is_authenticated:
        return JsonResponse({
            "success": False,
            "error": _("You need to be authenticated to use this feature.")
        }, status=200)

    # Get the postcode and home number from the request
    postcode: str = request.GET.get('postcode',
        request.POST.get('postcode', "")
    )
    home_number: str = request.GET.get('home_number',
        request.POST.get('home_number', "")
    )
    postcode = postcode.strip()
    home_number = home_number.strip()

    # Check if the required fields are present
    if not all([postcode, home_number]):
        return JsonResponse({
            "success": False,
            "error": _("Missing required fields: postcode, home_number")
        }, status=200)

    # Get the address information
    try:
        addr = address_check(
            postcode=postcode,
            number=home_number,
        )

    # The address is invalid or the endpoint returned an error
    except AddressValidationError as e:
        logger.error(f"An error occurred while checking the address: {e.message}")
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=200)

    # Return the address information
    return JsonResponse({
        "success": True,
        "data": {
            "home_number":  addr.home_number,
            "postcode":     addr.postcode,
            **addr.data,
        }
    })