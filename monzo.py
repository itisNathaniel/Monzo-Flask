from flask import *
from pymonzo import MonzoAPI
import babel.numbers
from decimal import *

app = Flask(__name__)

# Environment Variables
server = "127.0.0.1"

# Fetch credentials from file
clientID = 'user_id_goes_here'
authCode = 'access_token_goes_here'

# Connect to Monzo API through pymonzo
monzo = MonzoAPI(
    client_id=clientID,
    auth_code=authCode,
    )

# Homepage -- temporarily replaced by duplicate of accounts page
@app.route("/")
def home():
    accountsList = monzo.accounts();
    return render_template('me.html', name=(monzo.accounts()[1].description), accountsList=accountsList)

# Me page lists accounts
@app.route("/me")
def me():
    accountsList = monzo.accounts();
    return render_template('me.html', accountsList=accountsList)

# Transactions Page
@app.route("/transactions", methods=['POST'])
def transactions():
    accountNo = request.form["account_id"]
    accountID = accountNo;
    accountattempt = -1
    FriendlyName = 'You should never see this, something has gone wrong'
    for account in monzo.accounts():
        accountattempt = accountattempt + 1
        if (monzo.accounts()[accountattempt].id == accountID):
            FriendlyName = (monzo.accounts()[accountattempt].type)
        else:
            pass
    transactionlist = monzo.transactions(accountID); #  limit=3
    return render_template('transaction.html', transactionlist=transactionlist, accountID=accountID, FriendlyName=FriendlyName)

# Get Name of Merchant by requesting transaction
@app.context_processor
def shopname():
    def shop_name(thisTransaction):
        try:
            merchantname = (monzo.transaction(thisTransaction,expand_merchant=True).merchant.name)
            return merchantname;
        except:
            shopname = (monzo.transaction(thisTransaction,expand_merchant=True).description)
            return shopname

    return dict(shop_name=shop_name)

# Get Currency amount and convert it from GBP to regional symbol and get amount
@app.context_processor
def currency():
    def currency(thisTransaction):
        try:
            currencyAbb = monzo.transaction(thisTransaction,expand_merchant=True).currency
            currencyAmount = (monzo.transaction(thisTransaction,expand_merchant=True).amount)
            currencyAmount = (abs(currencyAmount/100))
            currencyAmount = babel.numbers.format_currency( Decimal( currencyAmount ), currencyAbb )
            return currencyAmount
        except:
            return 'error';
    return dict(currency=currency)

# Get shop logo 
@app.context_processor
def shoplogo():
    def shop_logo(thisTransaction):
        try:
            merchantlogo = (monzo.transaction(thisTransaction,expand_merchant=True).merchant.logo)
            if (merchantlogo == ''):
                staticOutgoing = 'static/arrow-circle-up.svg'
                return staticOutgoing
            else:
                return merchantlogo
            
        except:
            if ((monzo.transaction(thisTransaction,expand_merchant=True).amount) > 0):
                staticIncoming = 'static/arrow-circle-down.svg'
                return staticIncoming

            elif ((monzo.transaction(thisTransaction,expand_merchant=True).amount) < 0):
                staticOutgoing = 'static/arrow-circle-up.svg'
                return staticOutgoing

    return dict(shop_logo=shop_logo)

# date parsed
@app.context_processor
def dateofCreation():
    def dateCreated(thisTransaction):
        try:
            d = monzo.transaction(thisTransaction).created
            return d.strftime('%d/%m/%Y')
        except:
            pass
    return dict(dateCreated=dateCreated)

# shop location
@app.context_processor
def shopLocation():
    def shop_location(thisTransaction):
        try:
            shopLocation = (monzo.transaction(thisTransaction,expand_merchant=True).merchant.address.get("city"))
            return shopLocation;
        except:
            pass
    return dict(shop_location=shop_location)


# if errors out, likely due to not using a post request, so redirect the user back to 
# accounts page 
@app.errorhandler(405)
def server_error(e):
    accountsList = monzo.accounts();
    return redirect("/me")


if __name__ == "__main__":
    app.run(host=server, port=80, threaded=True)
