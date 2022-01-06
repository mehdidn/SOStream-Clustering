# SOStream-Clustering
SOStream Algorithm Clustering

\documentclass[a4paper, 12pt]{article}

% packages
\usepackage[table]{xcolor}
\usepackage{geometry}
\usepackage{amsmath}
\usepackage{tikz}
\usepackage{epigraph}
\usepackage{amsmath, amsthm, amscd, amsfonts, amssymb, graphicx}
\usepackage{listings}
\usepackage{hyperref}
\usepackage{xepersian}
\usepackage{authblk}
\usepackage{indentfirst}
\usepackage{tabularx}

% set font
\settextfont{IRLotus.ttf}
\DeclareFixedFont{\titlefont}{T1}{ppl}{b}{it}{0.5in}

% images folder path
\graphicspath{ {./images/} } 

% geometry definition
\geometry{
    a4paper,
    top=20mm,
    bottom =20mm,
    left=20mm,
    right=20mm
}

% commands
\renewcommand\epigraphflush{flushright}
\renewcommand\epigraphsize{\normalsize}
\setlength\epigraphwidth{0.7\textwidth}
\renewcommand\tabularxcolumn[1]{>{\Centering}m{#1}}

% define colors
\definecolor{titlepagecolor}{cmyk}{1,.60,0,.40}
\definecolor{tableShade}{gray}{0.9}

% define author
\makeatletter                       
\def\printauthor{                 
    {\large \@author}}              
\makeatother
\author
{
    مهدی دهقانی \\
    220797048 \\
    \vspace{10mm}
    \texttt{mehdi.dehghani@ut.ac.ir}\vspace{8pt}
    \texttt{mahdiazadi18@yahoo.com}\vspace{20pt}
}

\newcommand\titlepagedecoration{%
\begin{tikzpicture}[remember picture,overlay,shorten >= -10pt]

\coordinate (aux1) at ([yshift=-15pt]current page.north east);
\coordinate (aux2) at ([yshift=-410pt]current page.north east);
\coordinate (aux3) at ([xshift=-4.5cm]current page.north east);
\coordinate (aux4) at ([yshift=-150pt]current page.north east);

\begin{scope}[titlepagecolor!40,line width=12pt,rounded corners=12pt]
\draw
  (aux1) -- coordinate (a)
  ++(225:5) --
  ++(-45:5.1) coordinate (b);
\draw[shorten <= -10pt]
  (aux3) --
  (a) --
  (aux1);
\draw[opacity=0.6,titlepagecolor,shorten <= -10pt]
  (b) --
  ++(225:2.2) --
  ++(-45:2.2);
\end{scope}
\draw[titlepagecolor,line width=8pt,rounded corners=8pt,shorten <= -10pt]
  (aux4) --
  ++(225:0.8) --
  ++(-45:0.8);
\begin{scope}[titlepagecolor!70,line width=6pt,rounded corners=8pt]
\draw[shorten <= -10pt]
  (aux2) --
  ++(225:3) coordinate[pos=0.45] (c) --
  ++(-45:3.1);
\draw
  (aux2) --
  (c) --
  ++(135:2.5) --
  ++(45:2.5) --
  ++(-45:2.5) coordinate[pos=0.3] (d);   
\draw 
  (d) -- +(45:1);
\end{scope}
\end{tikzpicture}%
}

\begin{document}
\begin{titlepage}

\noindent
{
    \begin{center}
    \includegraphics[width=4cm, height=4cm]{images/tehran_uni_logo.png}
    \end{center}
    
    \begin{center}
    {\Huge{\textbf{به نام خدا}}}\\
    \end{center}
    \vspace{8mm}
    \Large\begin{center}
        عنوان: پیاده‌سازی الگوریتم SOStream
    \end{center}
    \Large\begin{center}
        درس: داده کاوی
    \end{center}
    \Large\begin{center}
        استاد درس: مهندس قاسمی
    \end{center}
}
\null\vfill
\vspace*{1cm}
\noindent
\hfill
\begin{minipage}{0.35\linewidth}
    \begin{flushright}
        \printauthor
    \end{flushright}
\end{minipage}
%
\begin{minipage}{0.02\linewidth}
    \rule{1pt}{125pt}
\end{minipage}
\titlepagedecoration
\end{titlepage}
    
\noindent\Large{\textbf{کلاس MicroCluster}}\\

\par\large{این کلاس نشان دهنده خوشه‌های برنامه است که ویژگی هایی مثل تعداد داده‌ها، شعاع، مرکز، زمان ساخت، آخرین زمان تغییر و لیست داده‌های درون آن دارد.}\\

\noindent\large{این کلاس از هفت متد تشکیل شده است: }

\begin{enumerate}
    \item \large{update\textunderscore last\textunderscore edited\textunderscore time|\\
    این متد آخرین زمان تغییر خوشه را به روز رسانی می‌کند.}
    \item \large{insert\\
    این متد داده جدید را به خوشه اضافه می‌کند.}
    \item \large{merge\textunderscore data\textunderscore points\\
    این متد برای ادغام دو لست داده به کار می‌رود.}
    \item \large{fading\\
    این متد برای محاسبه f(t) که مقدار از بین رفتن خوشه است به کار می‌رود.}
    \item \large{get\textunderscore radius\\
    متد گرفتن مقدار شعاع خوشه}
    \item \large{set\textunderscore radius\\
    متد برای مقداردهی یا تغییر شعاع خوشه}
    \item \large{get\textunderscore centroid\\
    متد گرفتن مرکز خوشه}
\end{enumerate}

\newpage

\noindent\Large{\textbf{کلاس SOStream}}\\

\par\large{این کلاس الگوریتم SOStream را پیاده‌سازی می‌کند و شامل متدهایی است که شبه کدهای آن‌ها را در فایل مقاله دیده‌ایم}\\

\noindent\large{این کلاس شامل متد های زیر می‌باشد:}

\begin{enumerate}
    \item \large{find\textunderscore neighbors\\
    این متد برای پیدا کردن همسایه‌های خوشه برنده است.}
    \item \large{find\textunderscore overlap\\
    این متد برای پیدا کردن همسایه‌های خوشه خوشه برنده که با آن همپوشانی دارند به کار می‌رود.}
    \item \large{merge\textunderscore clusters\\
    این متد برای ادغام خوشه برنده با خوشه‌هایی که با آن همپوشانی دارند به کار می‌رود.}
    \item \large{update\textunderscore cluster\\
    به روز رسانی خوشه برنده و همسایگان آن هنگام اضافه شدن داده جدید}
    \item \large{fading\textunderscore all\\
    این متد برای از بین بردان خوشه‌ها با استفاده از محاسبه مقدار f(t) و مقایسه آن با fade\textunderscore threshold به کار می‌رود.}
    \item \large{adjust\textunderscore centroid\\
    این متد برای تنظیم مرکز خوشه به کار می‌رود که در متد update\textunderscore cluster نیز استفاده شده است.}
    \item \large{insert\\
    این متد برای درج یک خوشه در لیست خوشه‌ها به کار می‌رود.}
    \item \large{get\textunderscore centroids\textunderscore of\textunderscore clusters\\
    این متد برای گرفتن لیست مراکز خوشه‌ها به کار می‌رود.}
    \item \large{calculate\textunderscore purity\\
    این متد برای محاسبه خلوص خوشه‌ها و داده‌ها در این الگوریتم به کار می‌رود.}
    \item \large{باقی متدها\\
    بقیه متدها برای گرفتن مقادیر مورد استفاده در الگوریتم هستند.}
\end{enumerate}

\newpage

\noindent\Large{\textbf{main.py}}\\

\par\large{این اسکریپت برای اجرای الگوریتم SOStream استفاده می‌شود. ابتدا دیتای مورد نظر را از فایل مربوطه می‌خوانیم و یک جایگشت رندوم روی آن اجرا می‌کنیم تا در زمان از بین بردن خوشه‌ها که نسبت به زمان ساخت و اضافه شدن خوشه‌ها و داده‌ها کار می‌کند به مشکلی بر نخوریم.}\\

\par\large{سپس مقادیر موردنیاز، نظیر آلفا، ،minPts ،merge\textunderscore threshold لاندا و fade\textunderscore threshold را نسبت به شرایط مختلف مقداردهی می‌کنیم و الگوریتم را به صورت زیر اجرا می‌کنیم.}\\

\par\large{هر داده موجود در دیتاست را بصورت تکی به برنامه وارد می‌کنیم و نسبت به حالت فعلی داده‌ها و خوشه‌ها، نسبت به به روز رسانی یا ادغام یا موارد دیگر اقدام می‌کنیم. هر 20 مرحله (هر بار که 20 داده به برنامه وارد شده باشد) نیز از بین بردن خوشه‌ها را طبق fading\textunderscore all انجام می‌دهیم و همچنین هر 25 مرحله نیز تعداد خوشه‌ها و مقدار خلوص را ذخیره می‌کنیم تا در انتها در نتیجه کار تغییرات آن‌ها را ببینیم.}\\

\par\large{با توجه به محاسبه شدن موارد مختلف در الگوریتم و ذخیره کردن تعداد خوشه‌ها و مقدار خلوص در هر 25 مرحله، می‌توانیم نمودار های خطی و میله‌ای متناسب با آن‌ها را نمایش بدهیم و همچنین بعد از آن، نتایجی مثل زمان پردازش، تعداد خوشه‌های نهایی، تعداد خوشه‌های از بین رفته، تعداد خوشه‌های ادغام شده و میانگین خلوص را نشان داده و بررسی میکنیم.}\\

\par\large{در ادامه مثال هایی از اجرا برنامه روی دو دیتاست قرار داده شده را میبینیم. بدیهی است که با تغییر مقادیر آلفا، لاندا، merge\textunderscore threshold یا ...، خروجی متفاوت خواهد شد. همچنین بخاطر جایگشت رندومی که در ابتدای کار روی دیتاست اعمال می‌شود نیز هر بار خروجی متفاوت خواهد بود.}\\

\par\large{در نمودارهای اول نقاط آبی رنگ، داده‌های ورودی و نقاط قرمز رنگ، مراکز خوشه‌های نهایی هستند.}\\

\newpage

\noindent\Large{\textbf{Dataset\textunderscore 1.csv}}\\

\begin{center}
    \includegraphics[width=17cm, height=8cm]{images/dataset1_values.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=14cm]{images/dataset1_data&clusters.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset1_numberOfClusters_line.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset1_numberOfClusters_bar.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset1_purity_line.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset1_purity_bar.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=8cm]{images/dataset1_results.png}
\end{center}

\newpage

\noindent\Large{\textbf{Dataset\textunderscore 2.csv}}\\

\begin{center}
    \includegraphics[width=17cm, height=8cm]{images/dataset2_values.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=14cm]{images/dataset2_data&clusters.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset2_numberOfClusters_line.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset2_numberOfClusters_bar.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset2_purity_line.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=12cm]{images/dataset2_purity_bar.png}
\end{center}

\begin{center}
    \includegraphics[width=17cm, height=8cm]{images/dataset2_results.png}
\end{center}
    
\end{document}
