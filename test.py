content = "document.querySelectorAll(\"input[data-testid='credit_card_number']\")[0].value='"+creditCard['cardNumber']+"';document.querySelectorAll(\"input[data-testid='credit_card_month']\")[0].value='"+cardExperied[0]+"';document.querySelectorAll(\"input[data-testid='credit_card_year']\")[0].value='" + \
    cardExperied[0]+"';document.querySelectorAll(\"input[data-testid='credit_card_security_code']\")[0].value='" + \
    creditCard['ccv'] + \
    "';document.querySelectorAll(\"input[data-testid='zipCode']\")[0].value='" + \
    creditCard['zipCode']+"';"
