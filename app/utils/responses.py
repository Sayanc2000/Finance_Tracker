from app.schemas import ErrorResponse
user_responses = {
    '404': {"model": ErrorResponse},
    '409': {"model": ErrorResponse},
    '401': {"model": ErrorResponse}
}