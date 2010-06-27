"""
 Routes to controllers
"""

urls = (
  '/', 'app.controllers.main.Index',
  '/export', 'app.controllers.main.Export',
  '/favorites', 'app.controllers.main.Favorites',
  '/topvoted', 'app.controllers.main.TopVoted',
  '/about', 'app.controllers.main.About',
  '/JsonQuestion','app.controllers.ajax.JsonQuestion',
  '/tags','app.controllers.ajax.Tags',
  '/quicklook','app.controllers.ajax.Quicklook',
  
)