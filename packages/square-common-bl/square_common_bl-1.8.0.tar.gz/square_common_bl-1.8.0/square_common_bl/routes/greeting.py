import json

from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse
from requests import HTTPError
from square_authentication_helper import TokenType
from square_commons import get_api_output_in_standard_format
from square_database_structure.square import global_string_database_name
from square_database_structure.square.greeting import global_string_schema_name
from square_database_structure.square.greeting.tables import Greeting

from square_common_bl.configuration import (
    global_object_square_logger,
    global_object_square_database_helper,
    global_object_square_authentication_helper,
)
from square_common_bl.messages import messages
from square_common_bl.pydantic_models.greeting import CreateGreetingV0

router = APIRouter(
    tags=["greeting"],
)


@router.post("/create_greeting/v0")
@global_object_square_logger.async_auto_logger
async def create_greeting_v0(body: CreateGreetingV0, access_token: str = Header(None)):
    greeting_is_anonymous = body.greeting_is_anonymous
    greeting_anonymous_sender_name = body.greeting_anonymous_sender_name
    greeting_text = body.greeting_text
    user_id = None
    try:

        """
        validation
        """
        # validate missing access token
        if not greeting_is_anonymous and access_token is None:
            output_content = get_api_output_in_standard_format(
                message=messages["GENERIC_400"],
                log="provide access_token for non-anonymous greetings.",
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=output_content,
            )
        # validate access token
        if not greeting_is_anonymous and access_token:
            access_token_payload = global_object_square_authentication_helper.validate_and_get_payload_from_token_v0(
                token_type=TokenType.access_token, token=access_token
            )[
                "data"
            ][
                "main"
            ]
            user_id = access_token_payload["user_id"]
        # validate extra params
        if greeting_is_anonymous and access_token is not None:
            output_content = get_api_output_in_standard_format(
                message=messages["GENERIC_400"],
                log="extra access_token provided for anonymous greeting.",
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=output_content,
            )
        if not greeting_is_anonymous and greeting_anonymous_sender_name is not None:
            output_content = get_api_output_in_standard_format(
                message=messages["GENERIC_400"],
                log="extra anonymous_sender_name provided for non anonymous greeting.",
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=output_content,
            )
        """
        main process
        """
        # add greeting to the table
        local_list = global_object_square_database_helper.insert_rows_v0(
            database_name=global_string_database_name,
            schema_name=global_string_schema_name,
            table_name=Greeting.__tablename__,
            data=[
                {
                    Greeting.greeting_is_anonymous.name: greeting_is_anonymous,
                    Greeting.greeting_anonymous_sender_name.name: greeting_anonymous_sender_name,
                    Greeting.user_id.name: user_id,
                    Greeting.greeting_text.name: greeting_text,
                },
            ],
        )

        """
        return value
        """

        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_CREATION_SUCCESSFUL"],
            data={"main": local_list["data"]["main"]},
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=output_content,
        )
    except HTTPError as http_error:
        global_object_square_logger.logger.error(http_error, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_error.response.status_code,
            content=json.loads(http_error.response.content),
        )
    except HTTPException as http_exception:
        global_object_square_logger.logger.error(http_exception, exc_info=True)
        """
        rollback logic
        """
        # pass
        return JSONResponse(
            status_code=http_exception.status_code, content=http_exception.detail
        )
    except Exception as e:
        """
        rollback logic
        """
        global_object_square_logger.logger.error(e, exc_info=True)
        output_content = get_api_output_in_standard_format(
            message=messages["GENERIC_500"],
            log=str(e),
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=output_content,
        )
