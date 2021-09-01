from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from . import portalview
from ecom.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

def contactindex(request):
    context = {}
    return render(request, 'portal/contact.html', context)

def sendemail(request):
    try:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        recepient = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        # message =message+'''
        # from '''+firstname+' '+lastname
        fullname = firstname+' '+lastname

        message = '''<!doctype html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
  <head>
    <title>
    </title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
      #outlook a{padding: 0;}
      			.ReadMsgBody{width: 100%;}
      			.ExternalClass{width: 100%;}
      			.ExternalClass *{line-height: 100%;}
      			body{margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;}
      			table, td{border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt;}
      			img{border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}
      			p{display: block; margin: 13px 0;}
    </style>
    <!--[if !mso]><!-->
    <style type="text/css">
      @media only screen and (max-width:480px) {
      			  		@-ms-viewport {width: 320px;}
      			  		@viewport {	width: 320px; }
      				}
    </style>
    <!--<![endif]-->
    <!--[if mso]> 
		<xml> 
			<o:OfficeDocumentSettings> 
				<o:AllowPNG/> 
				<o:PixelsPerInch>96</o:PixelsPerInch> 
			</o:OfficeDocumentSettings> 
		</xml>
		<![endif]-->
    <!--[if lte mso 11]> 
		<style type="text/css"> 
			.outlook-group-fix{width:100% !important;}
		</style>
		<![endif]-->
    <style type="text/css">
      @media only screen and (max-width:480px) {
      
      			  table.full-width-mobile { width: 100% !important; }
      				td.full-width-mobile { width: auto !important; }
      
      }
      @media only screen and (min-width:480px) {
      .dys-column-per-100 {
      	width: 100.000000% !important;
      	max-width: 100.000000%;
      }
      }
      @media only screen and (min-width:480px) {
      .dys-column-per-100 {
      	width: 100.000000% !important;
      	max-width: 100.000000%;
      }
      }
    </style>
  </head>
  <body>
    <div>
      <!--[if mso | IE]>
<table align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
<![endif]-->
      <div style='background:#4DBFBF;background-color:#4DBFBF;margin:0px auto;max-width:600px;'>
        <table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#4DBFBF;background-color:#4DBFBF;width:100%;'>
          <tbody>
            <tr>
              <td style='direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;'>
                <!--[if mso | IE]>
<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td style="vertical-align:top;width:600px;">
<![endif]-->
                <div class='dys-column-per-100 outlook-group-fix' style='direction:ltr;display:inline-block;font-size:13px;text-align:left;vertical-align:top;width:100%;'>
                  <table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'>
                    
                    <tr>
                      <td align='center' style='font-size:0px;padding:10px 25px;word-break:break-word;'>
                        <div style="color:#FFFFFF;font-family:'Droid Sans', 'Helvetica Neue', Arial, sans-serif;font-size:36px;line-height:1;text-align:center;">
                          Contact
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td align='center' style='font-size:0px;padding:10px 25px;word-break:break-word;'>
                        <div style="color:#ffffff;font-family:'Droid Sans', 'Helvetica Neue', Arial, sans-serif;font-size:16px;line-height:20px;text-align:center;">
                           From '''+fullname+''' <br> '''+message+''' <br> Email :- '''+recepient+'''
                        </div>
                      </td>
                    </tr>
                    
                  </table>
                </div>
                <!--[if mso | IE]>
</td></tr></table>
<![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]>
</td></tr></table>
<![endif]-->
      <!--[if mso | IE]>
<table align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
<![endif]-->
      <div style='background:#414141;background-color:#414141;margin:0px auto;max-width:600px;'>
        <table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#414141;background-color:#414141;width:100%;'>
          <tbody>
            <tr>
              <td style='direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;text-align:center;vertical-align:top;'>
                <!--[if mso | IE]>
<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td style="vertical-align:top;width:600px;">
<![endif]-->
                <div class='dys-column-per-100 outlook-group-fix' style='direction:ltr;display:inline-block;font-size:13px;text-align:left;vertical-align:top;width:100%;'>
                  <table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'>
                    <tr>
                      <td align='center' style='font-size:0px;padding:10px 25px;word-break:break-word;'>
                        <table border='0' cellpadding='0' cellspacing='0' style='cellpadding:0;cellspacing:0;color:#000000;font-family:Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;table-layout:auto;width:40%;' width='40%'>
                          <tbody>
                            <tr align='center'>
                              <td align='center'>
                                <a href='https://linkedin.com'>
                                  <img alt='linkedin' height='50px' src='https://swu-cs-assets.s3.amazonaws.com/OSET/neopolitan/linkedin.png' width='50px'>
                                </a>
                              </td>
                              <td align='center'>
                                <a href='https://facebook.com'>
                                  <img alt='facebook' height='50px' src='https://swu-cs-assets.s3.amazonaws.com/OSET/neopolitan/facebook.png' width='50px'>
                                </a>
                              </td>
                              <td align='center'>
                                <a href='https://twitter.com'>
                                  <img alt='twitter' height='50px' src='https://swu-cs-assets.s3.amazonaws.com/OSET/neopolitan/twitter.png' width='50px'>
                                </a>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </td>
                    </tr>
                  </table>
                </div>
                <!--[if mso | IE]>
</td></tr></table>
<![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]>
</td></tr></table>
<![endif]-->
      <!--[if mso | IE]>
<table align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;" width="600"><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
<![endif]-->
      <div style='background:#414141;background-color:#414141;margin:0px auto;max-width:600px;'>
        <table align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='background:#414141;background-color:#414141;width:100%;'>
          <tbody>
            <tr>
              <td style='direction:ltr;font-size:0px;padding:20px 0;padding-top:0px;text-align:center;vertical-align:top;'>
                <!--[if mso | IE]>
<table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td style="vertical-align:top;width:600px;">
<![endif]-->
                <div class='dys-column-per-100 outlook-group-fix' style='direction:ltr;display:inline-block;font-size:13px;text-align:left;vertical-align:top;width:100%;'>
                  <table border='0' cellpadding='0' cellspacing='0' role='presentation' style='vertical-align:top;' width='100%'>
                    <tr>
                      <td align='center' style='font-size:0px;padding:10px 25px;word-break:break-word;'>
                        <div style="color:#BBBBBB;font-family:'Droid Sans', 'Helvetica Neue', Arial, sans-serif;font-size:12px;line-height:1;text-align:center;">
                          View in Browser | Unsubscribe | Contact © 2019 All Rights Reserved
                        </div>
                      </td>
                    </tr>
                  </table>
                </div>
                <!--[if mso | IE]>
</td></tr></table>
<![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]>
</td></tr></table>
<![endif]-->
    </div>
  </body>
</html>'''

        # send_mail(subject, body, EMAIL_HOST_USER, [recepient], fail_silently = False)
        msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER])
        msg.attach_alternative(message, "text/html")
        msg.send()
        messages.success(request, "Mail send successfully")
    except Exception as e:
        messages.error(request, "Error: Message send failed. Reason:- "+str(e))
    finally:
        return redirect('/contactindex')