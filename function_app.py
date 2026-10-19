import logging
import azure.functions as func
import fetch_bysykkel_data as bysykkel

app = func.FunctionApp()

@app.timer_trigger(
    schedule="0 * * * * *",  # Every minute
    arg_name="timer",
    run_on_startup=False,
)
def capture_availability(timer: func.TimerRequest):
    bysykkel.capture_to_blob()