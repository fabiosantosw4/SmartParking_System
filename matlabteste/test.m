
clc
close all



text = '  d   h9 s9 sh';
tam_texto=numel(text);
i=0;
u=0;
    if tam_texto==6 || tam_texto>6
        while i<tam_texto
            i=i+1;
            if text(i)==32 || char(text(i))==' '    
            else
                u=u+1;
                disp(char(text(i)));
                text_a(u)=text(i);
            end 
        end
        disp(u)
    else
        disp("Tamanho invalido!");
    end
    

   
    text_final=sprintf('%c%c%c%c%c%c',text_a(1),text_a(2),text_a(3),text_a(4),text_a(5),text_a(6))