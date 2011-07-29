def dev_or_prod(request):
    import settings

    return {
        'is_prod':settings.IS_PROD
    }

