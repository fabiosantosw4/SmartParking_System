%text='dasdas'
text= sprintf('line1\nline 2\nline 3')
lines = strsplit(text, '\n');
lines(1)
tam_texto=numel(text);
i=0;
u=0;

found_f = false;
found_s = false;
if found_f==true && found_s==true
    text_final=sprintf('%c%c%c%c%c%c',text(first32-2),text(first32-1),text(first32+1),text(first32+2),text(second32+1),text(second32+2))
    else

    if tam_texto==6 || tam_texto>6
        while i<tam_texto
            i=i+1;
            if text(i)==32 || char(text(i))==' ' || isempty(char(text(i)))   
            else
                    u=u+1;
                    disp(char(text(i)));
                    text_a(u)=text(i);                    
            end 
        end
    else
        disp("Tamanho invalido!");
    end
    disp(u)
    tam_texto_a = numel(text_a)
    text_final=sprintf('%c%c%c%c%c%c',text_a(tam_texto_a-5),text_a(tam_texto_a-4),text_a(tam_texto_a-3),text_a(tam_texto_a-2),text_a(tam_texto_a-1),text_a(tam_texto_a));
end

disp(text_final)