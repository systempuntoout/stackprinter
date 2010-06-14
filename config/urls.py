"""
 Routes to controllers
"""

urls = (
  '/', 'controllers.main.Index',
  '/export', 'controllers.main.Export',
  '/favorites', 'controllers.main.Favorites',
  '/topvoted', 'controllers.main.TopVoted',
  '/about', 'controllers.main.About',
  '/JsonQuestion','controllers.ajax.JsonQuestion'
)