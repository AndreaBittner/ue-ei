%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%            Identification
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{isas-seminar}[2005/04/13 The ISAS seminar class]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%            Preliminary declarations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\cover}{}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{eso-pic}
\RequirePackage{fix-cm}
\RequirePackage{amsmath}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%            Options
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\eventtype#1{\gdef\@eventtype{#1}}
 \global\let\@eventtype\@empty
\DeclareOption{cover}{
  \def\gruppe#1{\gdef\@gruppe{#1}}
  \global\let\@gruppe\@empty
  \def\seminartitle#1{\gdef\@seminartitle{#1}}
  \global\let\@seminartitle\@empty
  \setlength\textwidth{16cm}

  \renewcommand{\cover}{
    \definecolor{covertextblue}{rgb}{0.4,0.4,0.6}
    \AddToShipoutPicture{
    \setlength{\unitlength}{1cm}
    \put(0.3,1){
    \includegraphics{isas-watermark.pdf}}
    }
    \pagestyle{empty}


    \vspace{-1cm}
    \fontfamily{phv}\fontseries{b}\color{covertextblue}
    \fontshape{sl}
    \begin{center}
      ~\\[1cm]
      \fontsize{25}{30}\selectfont
      \@eventtype\\
      \fontsize{34}{43}\selectfont
      \@seminartitle\\
      \fontsize{25}{30}\selectfont
      \@date\\
    \end{center}

    \fontseries{m}%
    \fontshape{n}
    \fontsize{25}{30}
    \color{covertextblue}
    \selectfont
    \begin{center}
      \rotatebox[origin=c,units=360]{30}{
        \hspace{-2.3cm}
        \setlength{\fboxrule}{2pt}
        \fbox{
          \begin{minipage}{20cm}
            \centering
            \@author\\
            \@title
          \end{minipage}
        }
        \setlength{\fboxrule}{1pt}
      }
    \end{center}
    \vspace{2cm}

    \clearpage
    \ClearShipoutPicture
    \pagecolor{white}
    \parbox{16cm}{}
    \clearpage
    \pagestyle{empty}
  }
}
\ProcessOptions\relax

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%           Main declarations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\LoadClass[twoside]{article}

\setlength{\parindent}{0em}
\setlength{\parskip}{1.5ex plus0.5ex minus0.2ex}
\renewcommand{\baselinestretch}{1.2}

\setlength{\fboxrule}{1pt}
\setlength{\fboxsep}{3mm}

\clubpenalty=100000
\widowpenalty=1000000
\brokenpenalty=1000000
\finalhyphendemerits=1000000


\renewcommand{\normalsize}{\fontsize{12pt}{14pt}\selectfont}
\RequirePackage[a4paper,hmargin=2cm,vmargin=1.5cm,includeheadfoot]{geometry}
\RequirePackage{ngerman}
\RequirePackage{fancyhdr}
\RequirePackage[pdftex,hypertexnames=false,colorlinks,linkcolor=black,citecolor=black]{hyperref}
\pagestyle{fancy}
\fancyhead[OR,EL]{\sffamily\footnotesize  Intelligente Sensor-Aktor-Systeme (ISAS), KIT}
\fancyhead[OL,ER]{\sffamily\footnotesize \@eventtype ~ \@seminartitle}
\fancyfoot[OR,EL]{\sffamily\small\thepage}
\fancyfoot[OC,EC]{\sffamily\footnotesize ISAS.uni-karlsruhe.de}
\renewcommand{\headrulewidth}{0.1pt}
\renewcommand{\footrulewidth}{0.1pt}

\RequirePackage[pdftex]{graphicx}
\RequirePackage{color}
\RequirePackage{float}
%\RequirePackage[float]{caption2}
\RequirePackage{caption}
\renewcommand*\captionfont{\sffamily}
\renewcommand*\captionlabelfont{\sffamily\bfseries}

\renewcommand{\maketitle}{%
  {
    \renewcommand{\baselinestretch}{1}
    \cover
    \fontsize{20}{22}
    %\huge
    \fontfamily{phv}\fontseries{bx}%
  \selectfont\normalcolor
  \thispagestyle{empty}
  \setcounter{page}{1}
  \begin{center}
    \@title\\
    \fontsize{18}{22}
    %\LARGE
    \fontfamily{phv}\fontseries{b}%
    \fontshape{sl}\selectfont\normalcolor
    \vspace{0.5ex}
     -- \@eventtype:~\@seminartitle --\\
    \vspace{1ex}
    \fontsize{16}{19}\fontfamily{phv}\fontseries{m}%
    \fontshape{n}\selectfont\normalcolor
    \@author\\
    \vspace{0.5ex}
    \fontsize{14}{17}\fontfamily{phv}\fontseries{m}%
    \fontshape{n}\selectfont\normalcolor
    \@date\\
    \vspace{1ex}
  \end{center}}
}

\renewenvironment{abstract}{%
  \normalsize
  \begin{center}%
    {\sffamily\bfseries\normalsize\abstractname}%\vspace{\z@}}%
  \end{center}%
  \quotation\vspace{-1cm}
  {\endquotation}
}


\renewcommand\section{\@startsection{section}{1}{\z@}%
                                   {-3.5ex \@plus -1ex \@minus -.2ex}%
                                   {2.3ex \@plus.2ex}%
                                   {\sffamily\Large\bfseries}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                   {-3.25ex\@plus -1ex \@minus -.2ex}%
                                   {1.5ex \@plus .2ex}%
                                   {\sffamily\large\bfseries}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                   {-3.25ex\@plus -1ex \@minus -.2ex}%
                                   {1.5ex \@plus .2ex}%
                                   {\sffamily\normalsize\bfseries}}%
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                   {3.25ex \@plus1ex \@minus.2ex}%
                                   {-1em}%
                                   {\sffamily\normalsize\bfseries}}
\renewcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}
                                   {3.25ex \@plus1ex \@minus .2ex}
                                   {-1em}
                                   {\sffamily\normalsize\bfseries}}

\def\rv#1{{\mathbf #1}} %Random Variable
\def\vec#1{\underline{#1}} %Vector
\def\rvv#1{{\vec{\rv{#1}}}} %Random Vector
\def\mat#1{{\mathbf #1}} %Matrix
\def\Var{\mathrm{Var}} %Variance
\def\E{\mathrm{E}} %Expectation
\def\Cov{\mathrm{Cov}} %Covariance
\def\IN{\mathrm{I\hspace{-2pt}N}} %Natural Numbers
\def\IR{\mathrm{I\hspace{-2pt}R}} %Real Numbers 