% Programa musica1.m
% Preparado por S. Scott Moor, IPFW  August 2004
% Baseado em sugestões de Shreekanth Mandayam, 
% Departamento de Engenharias Elétrica e da Computação, Rowan University
%   veja http://users.rowan.edu/~shreek/networks1/music.html
% Esse programa cria ondas senóides para séries de notas padrões.
%  Cada nota é configurada para ter uma duração de 0.5 segundos 
% e taxa de amostragem de 8000 Hz.  As notas são reunidas em uma
% música que então é reproduzido pelo computador.
% variáveis usadas: 
%	fa	= frequencia de amostragem (amostragens/seg)
%	t	= vetor tempo (seg.)
%	a, b, cs, d, e, & fs = a amplitude de uma série de notas usadas na música. 
% 	linha1, linha2, linha3 = a série de amplitudes usadas para cada linha da música.
%	song 	= the amplitude series for the entire song. 

% configuração das séries de tempo.
fa= 16000; %frequencia de amostragem
Ta=1/fa; %periodo de amostragem
t = [0:Ta:0.5]; %eixo do tempo, discretizado, total: 0.5 s

% defina cada nota individualmente
a=sin(2*pi*440*t);
b=sin(2*pi*493.88*t);
cs=sin(2*pi*554.37*t);
d=sin(2*pi*587.33*t);
e=sin(2*pi*659.26*t);
fs=sin(2*pi*739.99*t);

% montando as notas em uma música.
linha1 = [a,a,e,e,fs,fs,e,e];
linha2 = [d,d,cs,cs,b,b,a,a];
linha3 = [e,e,d,d,cs,cs,b,b];
musica = [linha1,linha2,linha3,linha3,linha1,linha2];

% agora tocando a música
soundsc(musica, fa)
filterBWInHz=80; %em Hz
windowShiftInms=10; %deslocamento da janela em ms
thresholdIndB=120; %limiar, abaixo disso, nao mostra
ak_specgram(musica,filterBWInHz,fa,windowShiftInms,thresholdIndB)
colorbar