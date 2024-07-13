#%%
import urllib.request
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from io import BytesIO

# Fetch image from URL with user-agent header
def fetch_image_from_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        image_data = response.read()
    return image_data

# URL of the image
image_url = 'https://1000logos.net/wp-content/uploads/2018/11/Capital-One-Logo.jpg'

# Fetch and open the image
image_data = fetch_image_from_url(image_url)

# Open image using matplotlib
image = plt.imread(BytesIO(image_data), format = 'jpg')

# Ensure the image is properly resized for better fit
imagebox = OffsetImage(image, zoom=0.025)
    
# Interest Revenue 
def calculate(product):
    # Extracting values from the dictionary
    creditLine = product["creditLine"]
    utilization = product["utilization"]
    interestRate = product["interestRate"]
    annualFee = product["annualFee"]
    annualOpsCost = product["annualOpsCost"]
    fundingCost = product["fundingCost"]
    chargeOff = product["chargeOff"]
    bookings = product["bookings"]
    remainingBalance = product["remainingBalance"]

    # Revenue
    revenuePerAccount = creditLine * utilization * interestRate # Credit Line * Utilization * Annual Interest Rate
    revenuePerAccount += annualFee # Add Annual Fee
    totalRevenue = revenuePerAccount * bookings # Multiply by Annual Bookings

    # Loss
    numberOfCustomersWhoArentPaying = chargeOff * bookings # Number of customers who don't pay
    loss = numberOfCustomersWhoArentPaying * remainingBalance # Loss from customers who don't pay their balance
    loss += fundingCost * utilization * creditLine * bookings # Funding Cost = Funding Cost Rate * Utilization * Credit Line * Bookings
    loss += annualOpsCost * bookings # Add Annual Ops Cost

    # Profit
    profit = totalRevenue - loss # Profit = Total Revenue - Total Loss
    return profit

def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.0fM' % (x * 1e-6)

def printProduct(product):
    pro = calculate(product)
    formatted_pro = '{:,}'.format(int(pro))
    print(f"Product {product['name']} profit: ${formatted_pro}")
    return pro

# Calculation for a 10k product
product_10k = {
    "creditLine": 10000,
    "utilization": 0.50,
    "interestRate": 0.10,
    "annualFee": 40,
    "annualOpsCost": 20,
    "fundingCost": 0.02,
    "chargeOff": 0.03,
    "bookings": 100000,
    "remainingBalance": 10000,
    "name" : "10k"
}

# Calculation for a 20k product
product_20k = {
    "creditLine": 20000,
    "utilization": 0.40, # 8k / 20k 
    "interestRate": 0.10,
    "annualFee": 40,
    "annualOpsCost": 20,
    "fundingCost": 0.02,
    "chargeOff": 0.03,
    "bookings": 100000,
    "remainingBalance": 20000,
    "name" : "20k"
}

# 10k
pro10k = printProduct(product_10k)

# 20k
pro20k = printProduct(product_20k)

# Plot data
colors = ['#D22E1E', '#004878']
plt.bar(("Product 10k", "Product 20k"), (pro10k, pro20k), color = colors)

# Set y-axis to start at 0
plt.ylim(bottom=0)

# Add labels and title
plt.xlabel('Products')
plt.ylabel('Profit ($)')
plt.title('Profit by Product')

# Format the y-axis to show dollar amounts in millions
formatter = FuncFormatter(millions)
plt.gca().yaxis.set_major_formatter(formatter)

# Add logo image to the plot
ab = AnnotationBbox(imagebox, (1, 1.1), frameon=False,
                    xycoords='axes fraction', boxcoords="axes fraction",
                    pad=0.0)

plt.gca().add_artist(ab)

# Display the graph
plt.show()

# %%
