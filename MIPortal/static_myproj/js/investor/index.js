function format_amount(number) {
    number = parseFloat(number)
    return number.toLocaleString('en-IN', {
        maximumFractionDigits: 2,
        style: 'currency',
        currency: 'INR'
    });
}