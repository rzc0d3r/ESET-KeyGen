## 1. Generation using implemented email APIs (Auto method, but less stable)
> If you use ```--email-api tempmail```, you need to have the cloudflare captcha solved!
> Then you need to press Enter after you see the email site, without fail (**[INPT]** console message type)!

> Also, if you see a message like **[INPT]** in the console, it means that you need to do keyboard input into the console!

> You can also try the command line argument ```--try-auto-cloudflare``` which will try to automatically pass cloudflare captcha!

<details>
  <summary>Example generation through --email-api tempmail</summary>
  
  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/key_run_win_tempmail.png)
</details>

---

<details>
  <summary>ESET HOME Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --account
  ```
  ```
  ESET-KeyGen_v1.4.7.0_win64.exe --chrome --account
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!

  2. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/account_run_win.png)
</details>

<details>
  <summary>Business ESET Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --business-account
  ```
  ```
  ESET-KeyGen_v1.4.7.0_win64.exe --chrome --business-account
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!
  
  > It is also recommended to use ```developermail```, ```guerrillamail```, ```10minutemail``` email api to generate such accounts. So if you are unable to generate this account, try different variations of the email APIs!

  2. Wait until appears you will see *"Solve the captcha on the page manually!!!"*. Next, you will see a captcha with text input in the browser window created. You solve it and then just do nothing, the algorithm will do everything for you!

  3. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/business_account_run_win.png)
</details>

## 2. Generation using your email provider (Totally manual method, but hyper stable)

<details>
  <summary>ESET HOME Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --account --custom-email-api
  ```
  ```
  ESET-KeyGen_v1.4.7.0_win64.exe --chrome --account --custom-email-api
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!

  2. Then in the console you'll see *"Enter an email address you have access to"* and you'll need to enter a real existing email address that you can read incoming emails to. I suggest using a temporary email for this, such as [TempMail](https://temp-mail.org)
  > Then the algorithm will continue as in the first method

  3. After some time in the console you will see the message *"Enter the link to activate your account, it will come to the email address you provide"*, here you need to go to your email and find mail in inbox (you will have to wait)
    
     **FROM: info@product.eset.com**
     
     **SUBJECT: Account Confirmation**

     Then open that email and copy the link that is in the button (right click on the button, copy link address) and paste it into the console. If you have done everything correctly, the generation will complete successfully!

     ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/activated_href_esethome.png)

  4. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/account_run_win_custom_email_api.png)
</details>

<details>
  <summary>Business ESET Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --business-account --custom-email-api
  ```
  ```
  ESET-KeyGen_v1.4.7.0_win64.exe --chrome --business-account --custom-email-api
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!

  2. Then in the console you'll see *"Enter an email address you have access to"* and you'll need to enter a real existing email address that you can read incoming emails to. I suggest using a temporary email for this, such as [TempMail](https://temp-mail.org)
  > Then the algorithm will continue as in the first method

  3. Wait until appears you will see *"Solve the captcha on the page manually!!!"*. Next, you will see a captcha with text input in the browser window created. You solve it and then just do nothing, the algorithm will do everything for you!

  4. After some time in the console you will see the message *"Enter the link to activate your account, it will come to the email address you provide"*, here you need to go to your email and find mail in inbox (you will have to wait)

     **FROM: noreply@eba.eset.com**

     **SUBJECT: ESET BUSINESS ACCOUNT - Account activation**

     Then open that email and copy the link that is in the button (right click on the button, copy link address) and paste it into the console. If you have done everything correctly, the generation will complete successfully!

     ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/activated_href_business.png)

  5. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/business_account_run_win_custom_email_api.png)
</details>
