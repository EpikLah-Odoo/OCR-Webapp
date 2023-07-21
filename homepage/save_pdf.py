import pysftp, os

def save_pdf(upfile):
  fss = FileSystemStorage(location='/root/file_upload/')
  file = fss.save(upfile.name, upfile)
  file_url = fss.url(file)
  return file