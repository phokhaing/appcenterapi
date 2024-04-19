#  +---------------------------------------------------------------------------------
#  | Copyright (c)ftb bank, 2023.
#  +---------------------------------------------------------------------------------
#  | NAME : PHO KHAING
#  | EMAIL: khaing.pho@ftb.com.kh
#  | DUTY : FTB BANK (HEAD OFFICE)
#  | ROLE : Full-Stack Software Developer
#  +---------------------------------------------------------------------------------
#  | Released 20.08.2023.
#  | Description: This class provides methods for generating consistent API responses.
#  +---------------------------------------------------------------------------------

from rest_framework import status
from rest_framework.response import Response


class ApiResponse:
    # ----------------------------------------------------------------
    # Method: success
    # Description: Create a successful API response.
    # Params:
    #   - results: The results to include in the response (default: None).
    #   - message: A message describing the success (default: "Request successful.").
    #   - status_code: The HTTP status code (default: 200 OK).
    # ----------------------------------------------------------------
    @staticmethod
    def success(
        status_code=status.HTTP_200_OK,
        message="Resource retrieved successfully",
        results=[],
        paginators=None,
        count=None,
        next=None,
        previous=None,
    ):
        context = {
            "success": True,
            "status": status_code,
            "message": message,
            "count": count,
            "next": next,
            "previous": previous,
            "results": results,
        }

        if results is not None:
            context["results"] = results

        if paginators is not None:
            context["paginators"] = paginators

        return Response(context, status=status_code)

    # ----------------------------------------------------------------
    # Method: created
    # Description: Create a successful API response for resource creation.
    # Params:
    #   - data: The data to include in the response (default: None).
    #   - message: A message describing the success (default: "Resource created successfully.").
    # ----------------------------------------------------------------
    @staticmethod
    def created(
        status_code=status.HTTP_201_CREATED,
        message="Resource created successfully.",
        results=None,
    ):
        return ApiResponse.success(
            results=results, message=message, status_code=status_code
        )

    # ----------------------------------------------------------------
    # Method: no_content
    # Description: Create a 204 No Content response with an optional message.
    # Params:
    #   - message: A message describing the success (default: "Request processed successfully with no content.").
    # ----------------------------------------------------------------
    @staticmethod
    def no_content(
        status_code=status.HTTP_204_NO_CONTENT,
        message="Request processed successfully with no content.",
    ):
        return Response({"message": message}, status=status_code)

    # ----------------------------------------------------------------
    # Method: error
    # Description: Create an error API response.
    # Params:
    #   - message: A message describing the error (default: "Bad Request").
    #   - status_code: The HTTP status code (default: 400 Bad Request).
    #   - errors: Additional error details (default: None).
    # ----------------------------------------------------------------
    @staticmethod
    def error(
        status_code=status.HTTP_400_BAD_REQUEST,
        message="Fail, bad reequest",
        errors=None,
    ):
        response_data = {
            "success": False,
            "status": status_code,
            "message": message,
        }
        if errors is not None:
            response_data["errors"] = errors

        return Response(response_data)

    # ----------------------------------------------------------------
    # Method: not_found
    # Description: Create a 404 Not Found error response.
    # Params:
    #   - message: A message describing the error (default: "Resource not found").
    # ----------------------------------------------------------------
    @staticmethod
    def not_found(
        status_code=status.HTTP_404_NOT_FOUND, message="Resource not found", errors=None
    ):
        return ApiResponse.error(
            message=message, status_code=status_code, errors=errors
        )
