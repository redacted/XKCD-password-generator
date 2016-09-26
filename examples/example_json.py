from xkcdpass import xkcd_password as xp
from django.http import JsonResponse


def json_password_generator(request):
    # Example Django view to generate passphrase suggestions via xkcd library
    # Called with optional params e.g.
    # /json_password_generator/?tc=true&separator=|&acrostic=face

    if request.method == 'GET':
        acrostic = request.GET.get("acrostic", None)
        titlecase = request.GET.get("tc", None)

        wordfile = xp.locate_wordfile()
        words = xp.generate_wordlist(
            wordfile=wordfile,
            min_length=3,
            max_length=8)
        suggestion = xp.generate_xkcdpassword(words, acrostic=acrostic)

        if titlecase:
            # Convert "foo bar" to "Foo Bar"
            suggestion = suggestion.title()

        return JsonResponse({
            'suggestion': suggestion}
            )
