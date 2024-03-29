# Operating System CPU Scheduler
This is a simulation of how CPU scheduler assignes tasks for a multi-core system.

We define tasks and their priorities along with duration and type. We assume that we have four cores and apply SJF (Shortest Job First), RR (Round Robin), FCFS (First Come First Served) algorithms. 

## My Project Description for Uni

این برنامه با استفاده از الگوریتم های (FCFS,SJF,RR) یک سیستم زمان بندی وظایف اولیه را شبیه سازی می کند. کلاس "Task" را با ویژگی هایی مانند نام، نوع، مدت زمان، منابع، وضعیت، زمان اجرا و اولویت تعریف می کنیم. منطق زمان‌بندی با استفاده از الگوریتم ها ذکر شده در تابع مشخص پیاده‌سازی
می‌شود، که اجرای وظایف را از طریق رشته‌هایی که برای هر پردازنده طراحی شده، مدیریت می‌کند و با استفاده از قفل ها همگام سازی میان نخ ها صورت میگیرد. تابع اصلی ورودی کاربر را برای منابع و وظایف جمع آوری می کند، وظایف را مقداردهی اولیه می کند و آنها را به یک صف آماده اضافه می کند. یک رشته چاپی به طور همزمان نتایج اجرا را نمایش می دهد. الگوریتم ها ذکر شده اجرای کار را شبیه سازی می کند و برنامه با چاپ نتایج نهایی به پایان می رسد. همچنین می‌توان تعداد پردازنده ها و سایر پارامترها را برای مطابقت با پیکربندی‌های خاص سیستم انجام داد.


الگوریتم SJF:

در فایل SJF.py با استفاده از resource allocation و aging، پیاده سازی SJF را شبیه سازی کردیم. به دلیل استفاده از الگوریتم SJF، اولویت پراسس هارا duration و مدت زمانشان قرار میدهیم. در این برنامه هر thread نمایانگر یک core میباشد که یک تسک را انجام میدهد.
در این برنامه پس از دریافت ورودی برای هر تسک، شی از کلاس Task برای آن ایجاد میکنیم که شامل ویژگی هایی از جمله اسم، نوع تسک، منابع مورد نیاز آن، اولویت و ... میباشد. core ها را با kernel_threads که یک لیست میباشد نشان میدهیم و ترد دیگری برای چاپ خروجی تعریف میکنیم. سپس ترد های کرنل را start کرده و به دنبال آن ترد چاپ خروجی را آغاز میکنیم. برنامه پس از جوین شدن تمام ترد ها داخل حلقه تمام میشود. تسکی که هر ترد انجام میدهد به این صورت است که ابندا exit_event را برای set() نبودنش چک میکند (به این معنی که برنامه تمام نشده). و داخل این حلقه تسکی را از صف ready برداشته و منابع آن را بررسی میکند. اگر این منابع در دسترس نباشد، این تسک از حالت running خارج شده و وارد حالت waiting میشود و در صف waiting قرار داده میشود. در این بخش برای جلوگیری از وقوع starvation نیز چک میکنیم که اگر تعداد دفعاتی که این تسک در حالت انتظار رفته بیش از سه باشد، به اولویت آن یکی اضافه میشود. در نهایت پس از اینکه یک core، تسک را انجام داد، منابعی که allocate شده بودند آزاد میشوند. در اگر هر چهار core در حال انجام تسک باشد داخل یک timeUnit، آنگاه event برای پرینت set میشود و ترد print_results که منتظر این event بود برای چاپ خروجی فعال میشود.



الگوریتم RR:

در فایل RR.py زمانبندی  تعدادی task را با استفاده ازresource allocation  و thread و الگوریتم Round Robin با quantum=3  پیاده سازی می کند. این برنامه شامل یک کلاس Task است که شامل ویژگی هایی از جمله اسم، نوع تسک، منابع مورد نیاز آن، اولویت و ... میباشد. همگام سازی از طریق یک mutex برای مدیریت منابع مشترک و جلوگیری از race condition در برنامه ریزی ، به دست می آید. توابع chekingForAvalibleResources , assignResources منابع را بررسی و تخصیص می دهند، همچنین تابع waitingtoReady وظایف را از waiting queue به ready queue بر اساس در دسترس بودن منابع انتقال می دهد. تابع execute_task با در نظر گرفتن در دسترس بودن منابع و کوانتوم زمانی مشخص، اجرای کار را بر روی چندین هسته شبیه سازی می کند. تابع print_results وضعیت در حال تکامل هر هسته را در طول زمان چاپ می‌کند و از یک mutex برای همگام‌سازی استفاده می‌کند. تابع main ورودی کاربر را برای منابع و جزئیات هر task دریافت میکند و انها را در readyqueue که از نوع PriorityQueue میباشد قرار میدهد، و سپس چهار thread به ازای هر هسته و یک thread مشترک برای چاپ خروجی نخ ها ایجاد میکند . 


الگوریتم FCFS:

فایل FCFS.py زمانبندی  تعدادی task را با استفاده ازresource allocation  و thread و queue و mutex lock و الگوریتم FCFS(first call first serviced) پیاده سازی می کند. این برنامه شامل یک کلاس Task است که شامل ویژگی هایی مشابه فایل RR.py می باشد . همچون فایل RR.py این کد شامل توابعی برای بررسی در دسترس بودن منابع(chekingForAvalibleResources)، تخصیص منابع(, assignResources)، انتقال وظایف بین حالت‌های انتظار و آماده(waitingtoReady)، و اجرای وظایف (execute_task) روی هسته‌ها است.صف های ready queue و waiting queue از نوع queue هستند. . تابع print_results وضعیت در حال تکامل هر هسته را در طول زمان چاپ می‌کند و از یک mutex برای همگام‌سازی استفاده می‌کند. تابع main ورودی کاربر را برای منابع و جزئیات هر task دریافت میکند و انها را در readyqueue قرار میدهد، و سپس چهار thread به ازای هر هسته و یک thread مشترک برای چاپ خروجی نخ ها ایجاد میکند . 
