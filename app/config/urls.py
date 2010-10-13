"""
 Routes to controllers
"""

urls = (
  '/', 'app.controllers.main.Index',
  '/export', 'app.controllers.main.Export',
  '/topprinted', 'app.controllers.main.TopPrinted',
  '/favorites', 'app.controllers.main.Favorites',
  '/topvoted', 'app.controllers.main.TopVoted',
  '/about', 'app.controllers.main.About',
  '/question','app.controllers.ajax.Question',
  '/tags','app.controllers.ajax.Tags',
  '/quicklook','app.controllers.ajax.Quicklook',
)