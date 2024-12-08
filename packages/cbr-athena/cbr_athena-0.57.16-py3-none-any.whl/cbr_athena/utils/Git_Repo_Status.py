# from cbr_athena.api.GitHub_Rest_API import GitHub_Rest_API
#
#
# class Git_Repo_Status:
#
#     def __init__(self):
#         self.cbr_athena       = GitHub_Rest_API("the-cyber-boardroom/cbr-athena"      )
#         self.cbr_website_beta = GitHub_Rest_API("the-cyber-boardroom/cbr-website-beta")
#
#     def get_status(self):
#         return { "cbr-athena"      : self.get_status_cbr_athena      () ,
#                  "cbr-website-beta": self.get_status_cbr_website_beta() }
#
#     def get_status_cbr_athena(self):
#         return self.get_status_for_repo(self.cbr_athena     , 'cbr_athena/version'      , 'NWP3YE7FXK')
#
#     def get_status_cbr_website_beta(self):
#         return self.get_status_for_repo(self.cbr_website_beta, 'cbr_website_beta/version','NZDJOJ2CYH')
#
#     def get_status_for_repo(self, target_repo, version_file, badge_codecov_io):
#         version = target_repo.file_download(version_file).strip()
#         commits = target_repo.commits()
#         repo    = target_repo.repo()
#         return { "badge_codecov_io" : badge_codecov_io   ,
#                  "commits"          : commits            ,
#                  "description"      : repo.description   ,
#                  "name"             : repo.name          ,
#                  "last_modified"    : repo.last_modified ,
#                  "version"          : version            ,
#                  "url"              : repo.html_url      }