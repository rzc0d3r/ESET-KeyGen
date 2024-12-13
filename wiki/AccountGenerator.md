## 1. How to generate multiple accounts per run
Add a command-line argument: ```--repeat {number}```

```{number}``` - instead enter the number of accounts from **1** to **10**

---

## 2. Generation using implemented email APIs
> Also, if you see a message like **[INPT]** in the console, it means that you need to do keyboard input into the console!

---

<details>
  <summary>ESET HOME Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --account
  ```
  ```
  ESET-KeyGen_v1.5.3.3_win64.exe --chrome --account
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!

  2. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/account_run_win.png)
</details>

<details>
  <summary>ESET ProtectHub Account </summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --business-account
  ```
  ```
  ESET-KeyGen_v1.5.3.3_win64.exe --chrome --protecthub-account
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!
  
  > **Works ONLY if you use the ```--custom-email-api``` argument or the following ```Email APIs```: ```mailticking```, ```fakemail```**

  2. Wait until appears you will see *"Solve the captcha on the page manually!!!"*. Next, you will see a captcha with text input in the browser window created. You solve it and then just do nothing, the algorithm will do everything for you!

  3. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/protecthub_account_run_win.png)
</details>

## 3. Generation using your email provider

<details>
  <summary>ESET HOME Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --account --custom-email-api
  ```
  ```
  ESET-KeyGen_v1.5.3.3_win64.exe --chrome --account --custom-email-api
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
  <summary>ESET ProtectHub Account</summary>
  
  1. Run main.py or executable file use [MBCI](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/wiki/MBCI-Inferface.md):
  ```
  python main.py --chrome --protecthub-account --custom-email-api
  ```
  ```
  ESET-KeyGen_v1.5.3.3_win64.exe --chrome --protecthub-account --custom-email-api
  ```
  > File name is unique for each version! Do not copy the above command. This is an example!

  2. Then in the console you'll see *"Enter an email address you have access to"* and you'll need to enter a real existing email address that you can read incoming emails to. I suggest using a temporary email for this, such as [TempMail](https://temp-mail.org)
  > Then the algorithm will continue as in the first method

  3. Wait until appears you will see *"Solve the captcha on the page manually!!!"*. Next, you will see a captcha with text input in the browser window created. You solve it and then just do nothing, the algorithm will do everything for you!

  4. After some time in the console you will see the message *"Enter the link to activate your account, it will come to the email address you provide"*, here you need to go to your email and find mail in inbox (you will have to wait)

     **FROM: noreply@protecthub.eset.com**

     **SUBJECT: Welcome to ESET PROTECT Hub**

     Then open that email and copy the link that is in the button (right click on the button, copy link address) and paste it into the console. If you have done everything correctly, the generation will complete successfully!

     ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/activated_href_protecthub.png)

  5. Wait until you will see the account data
  > This information will also be written to a file named "Today date - ESET ACCOUNTS.txt"

  ![Windows](https://github.com/rzc0d3r/ESET-KeyGen/blob/main/img/protecthub_account_run_win_custom_email_api.png)
</details>
