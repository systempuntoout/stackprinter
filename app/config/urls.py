"""
 Routes to controllers
"""

urls = (
  '/', 'app.controllers.main.Index',
  '/export', 'app.controllers.main.Export',
  '/topprinted', 'app.controllers.main.TopPrinted',
  '/deleted', 'app.controllers.main.Deleted',
  '/favorites', 'app.controllers.main.Favorites',
  '/topvoted', 'app.controllers.main.TopVoted',
  '/about', 'app.controllers.main.About',
  '/question','app.controllers.ajax.Question',
  '/tags','app.controllers.ajax.Tags',
  '/quicklook','app.controllers.ajax.Quicklook',
  '/admin','app.controllers.admin.Admin',
  '/admin/authtokenrenewal','app.controllers.admin.AuthTokenRenewal',
  '/admin/topquestionsretriever','app.controllers.admin.TopQuestionsRetriever',
  '/_ah/warmup','app.controllers.admin.Warmup',
  '/sitemap_(\d+).xml', 'app.controllers.main.Sitemap',
  '/sitemap_index.xml', 'app.controllers.main.SitemapIndex',
)

"""
Static high traffic questions
"""
static_questions = {
    'stackoverflow_234075':'/questions/what-is-your-best-programmer-joke.html',
    'stackoverflow_102714':'/questions/what-was-your-first-home-computer.html',
    'stackoverflow_84556':'/questions/what-your-favorite-programmer-cartoon.html',
    'stackoverflow_192793':'/questions/what-is-your-favorite-programmer-t-shirt.html',
    'stackoverflow_2420689':'/questions/surprise-for-a-programmer-on-birthday.html',
    'serverfault_45734':'/questions/the-coolest-server-names.html',
    'stackoverflow_184618':'/questions/what-is-the-best-comment-in-source-code-you-have-ever-encountered.html',
    'gaming.stackexchange_2785':'/questions/are-there-any-similar-games-to-sim-tower.html',
    'stackoverflow_58640':'/questions/great-programming-quotes.html',
    'stackoverflow_895296':'/questions/how-can-you-tell-if-a-person-is-a-programmer.html',
    'stackoverflow_2187':'/questions/essential-programming-tools.html',
    'stackoverflow_282329':'/questions/what-are-five-things-you-hate-about-your-favorite-language.html',
    'stackoverflow_78756':'/questions/what-do-you-use-to-keep-notes-as-a-developer.html',
    'stackoverflow_1644':'/questions/what-good-technology-podcasts-are-out-there.html',
    'stackoverflow_687':'/questions/keyboard-for-programmers.html' 
}