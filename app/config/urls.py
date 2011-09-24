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