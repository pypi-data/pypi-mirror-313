from string import Template


HTML_EMAIL_TEMPLATE = Template("""

        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hi, $first_name, $last_name</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 14px; line-height: 1.5; color: #000; background-color: #f4f4f4; margin: 0; padding: 0;">
    <table cellpadding="0" cellspacing="0" style="width: 100%; max-width: 600px; margin: 0 auto; padding: 40px 20px;">
        <tr>
            <td>
                <table cellpadding="0" cellspacing="0" style="width: 100%; border-collapse: separate; border: 1px solid #e5e5e5; border-radius: 5px; background-color: #ffffff;">
                    <tr>
                        <td style="padding: 40px;">
                            <h1 style="font-size: 24px; font-weight: bold; margin-top: 0; margin-bottom: 24px;">Hi, $first_name $last_name</h1>
                                                        
                            <p style="margin-bottom: 24px;">Your Argilla account has been created. Here are your login details:</p>
                            
                            <table cellpadding="0" cellspacing="0" style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
                                <tr>
                                    <td style="padding: 12px 0; border-bottom: 1px solid #eaeaea;">
                                        <strong>URL:</strong>
                                    </td>
                                    <td style="padding: 12px 0; border-bottom: 1px solid #eaeaea;">
                                        <a href="$argilla_url" style="color: #0070f3; text-decoration: none;">$argilla_url</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 0; border-bottom: 1px solid #eaeaea;">
                                        <strong>Username:</strong>
                                    </td>
                                    <td style="padding: 12px 0; border-bottom: 1px solid #eaeaea;">
                                        $username
                                    </td>
                                </tr>

                                  <tr>
                                    <td style="padding: 12px 0; border-bottom: 1px solid #eaeaea;">
                                        <strong>Workspace:</strong>
                                    </td>
                                    <td style="padding: 12px 0; border-bottom: 1px solid #eaeaea;">
                                        $workspace
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 12px 0;">
                                        <strong>Password:</strong>
                                    </td>
                                    <td style="padding: 12px 0;">
                                        $password
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin-bottom: 24px;">If you have any questions or need assistance, please don't hesitate to reach out.</p>
                            
                            <p style="margin-bottom: 0;">Best regards</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>""")