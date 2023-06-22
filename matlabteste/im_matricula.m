function im_matricula(in_image)
try
    close all
    imagen=imread(in_image);
    figure(1)
    imshow(imagen);
    title('INPUT IMAGE WITH NOISE')
    %%Convert to gray scale
    if size(imagen,3)==3 % RGB image
        imagen=rgb2gray(imagen);
    end
    %%Convert to binary image
    threshold = graythresh(imagen);
    imagen =~imbinarize(imagen,threshold);
    %%Remove all object containing fewer than 30 pixels
    imagen = bwareaopen(imagen,60);
    pause(1)
    %%Show image binary image
    figure(2)
    imshow(~imagen);
    title('INPUT IMAGE WITHOUT NOISE')
    %%Label connected components
    [L Ne]=bwlabel(imagen);
    %%Measure properties of image regions
    propied=regionprops(L,'BoundingBox');
    hold on
    %%Plot Bounding Box
    for n=1:size(propied,1)
        rectangle('Position',propied(n).BoundingBox,'EdgeColor','g','LineWidth',2)
    end
    hold off
    pause (1)
    %%Objects extraction
    %figure
    for n=1:Ne
        [r,c] = find(L==n);
        n1=imagen(min(r):max(r),min(c):max(c));
        BW1 = imclose(n1, strel('square',4));
        results = ocr(BW1, 'CharacterSet', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789');
        disp(results.Text);
        if  ~isempty(results.Text) && n==1
            a=results.Text;
        end
        %imshow(BW1);
        %subplot(6,6,n)
        %pause(0.5)
    end

    b=sprintf(a);
    lines = strsplit(b, '\n');
    Linha1=lines(1);

    text=cell2mat(Linha1);
    disp('aaaaaaaaa:')
    disp(text)
    charArray = char(zeros(1, length(text)));

    found_f = false;
    for i = 1:length(text)
        if text(i)==32
            first32=i;
            found_f = true;
            break;
        end
    end

    found_s = false;
    if ~exist('first32', 'var')
    first32 = 0;
    end
    for i = (first32+1):length(text)
        if text(i)==32
            found_s = true;
            second32=i;
            break;
        end
    end

    tam_texto=numel(text);
    i=0;
    u=0;

    if found_f==true && found_s==true
        text_final=sprintf('%c%c%c%c%c%c',text(first32-2),text(first32-1),text(first32+1),text(first32+2),text(second32+1),text(second32+2));
    else

        if tam_texto==6 || tam_texto>6
            while i<tam_texto
                i=i+1;
                if text(i)==32
                else
                    u=u+1;
                    disp(char(text(i)));
                    text_a(u)=text(i);
                end
            end
        else
            error('Tamanho inválido!');
        end
        disp(u)
        tam_texto_a = numel(text_a);
        text_final=sprintf('%c%c%c%c%c%c',text_a(tam_texto_a-5),text_a(tam_texto_a-4),text_a(tam_texto_a-3),text_a(tam_texto_a-2),text_a(tam_texto_a-1),text_a(tam_texto_a));
    end

    disp(text_final)


    filename = 'C:\ProjetoVA_VS\yolov5-master\matlabteste\matricula.txt';
    if exist(filename, 'file') ~= 2
        % Arquivo não existe, cria novo arquivo
        fileID = fopen(filename, 'w+');
        if fileID == -1
            error('Não foi possível criar o arquivo.');
        else
            fprintf(fileID, 'Este é um novo arquivo.\n');
            fclose(fileID);
        end
    end

    % Abre o arquivo e escreve texto
    fileID = fopen(filename, 'w+');
    if fileID == -1
        error('Não foi possível abrir o arquivo.');
    else
        fprintf(fileID, '%s',text_final);
        fclose(fileID);
    end
catch exception
    disp(['Erro: ' exception.message]);
    close(gcf);
    close all;
    return;
    error('Script encerrado devido a um erro.');
end
end
