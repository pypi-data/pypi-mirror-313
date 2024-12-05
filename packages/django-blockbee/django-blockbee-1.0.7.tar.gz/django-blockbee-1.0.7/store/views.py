from django.shortcuts import render, redirect
from blockbee.models import Request, Provider
from blockbee.utils import get_active_providers, build_callback_url, generate_nonce
from blockbee.blockbee import get_address, get_conversion, get_qrcode
from blockbee import Invoice
from blockbee.apikey import apikey


def request(_r):
    coins = get_active_providers()

    if _r.POST:
        coin = _r.POST.get('coin', None)
        value = get_conversion('eur', coin, _r.POST.get('value'), apikey=apikey)['value_coin']
        order_id = _r.POST.get('order_id')

        invoice = Invoice(
            request=_r,
            order_id=order_id,
            coin=coin,
            value=value
        )

        payment_address = invoice.request()

        if payment_address is not None:
            return redirect('store:payment', request_id=payment_address.id)

    return render(_r, 'request.html', context={'select': coins})


def payment(_r, request_id):
    try:
        req = Request.objects.get(id=request_id)
        coin = req.provider.coin

        qrcode = get_qrcode(coin, req.address_in, apikey=apikey)

        fiat = get_conversion(coin, 'eur', req.value_requested, apikey=apikey)  # change 'eur' to the fiat of your needs

        ctx = {
            'req': req,
            'qrcode': qrcode,
            'fiat': fiat['value_coin']
        }

        return render(_r, 'payment.html', context=ctx)

    except Request.DoesNotExist:
        pass

    return redirect('store:request')
