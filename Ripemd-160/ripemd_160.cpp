#include <fstream>
#include <math.h>
#include <vector>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string.h>
#include <stdint.h>
using namespace std;

unsigned long f(int j,unsigned long x, unsigned long y, unsigned long z)
{
	unsigned long res;
	if ( j >= 0 && j <= 15)
		res = x ^ y ^ z;

	if ( j >= 16 && j <= 32)
		res = (x&y)|((~x)&z);

	if ( j >= 32 && j <= 47)
		res = (x | (~y)) ^ z;

	if ( j >= 48 && j <= 63)
		res = (x&z) | (y&(~z));

	if ( j >= 64 && j <= 79)
		res = x^(y|(~z));
	return res;
}

unsigned long K1 (int j)
{
	//левая ветка
	if(j >= 0 && j < 16)
		return 0x00000000;
	
	if(j >= 16 && j < 32)
		return 0x5A827999;

	if(j >= 32 && j < 48)
		return 0x6ED9EBA1;

	if(j >= 48 && j < 64)
		return 0x8F1BBCDC;

	if(j >= 64 && j < 80)
		return 0xA953FD4E;
	
}
	//правая ветка
unsigned long K2 (int j)
{
	if(j >= 0 && j < 16)
		return 0x50A28BE6;
	
	if(j >= 16 && j < 32)
		return 0x5C4DD124;

	if(j >= 32 && j < 48)
		return 0x6D703EF3;

	if(j >= 48 && j < 64)
		return 0x7A6D76E9;

	if(j >= 64 && j < 80)
		return 0x00000000;
}

unsigned long cir_shift(unsigned long val, int bits)
{
	return ((val << bits) & 0xFFFFFFFF) | ((val & 0xFFFFFFFF) >> (32 - bits));
}

unsigned long inv(unsigned long value)
{
    unsigned long res = 0;

    res |= ((value >> 0) & 0xFF) << 24;
    res |= ((value >> 8) & 0xFF) << 16;
    res |= ((value >> 16) & 0xFF) << 8;
    res |= ((value >> 24) & 0xFF) << 0;


    return res;
}

const char* Ripemd(unsigned char *AlignmentMsg,int size)
{
	
	//выбор 32-битных слов из сообщения
	unsigned long R1[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
                          7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
                          3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
                          1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
                          4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13};

	unsigned long R2[] = {5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
                          6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
                          15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
                          8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
                          12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11 };
	
	//набор для битового поворота влево
	unsigned long S1[] = {11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
                          7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
                          11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
                          11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
                          9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6 };

	unsigned long S2[] = {8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
                          9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
                          9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
                          15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
                          8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11 };
	
	//исходные значения слов дайджеста
	unsigned long* buf = new unsigned long[5];
	buf[0] = 0x67452301;
	buf[1] = 0xEFCDAB89;
	buf[2] = 0x98BADCFE;
	buf[3] = 0x10325476;
	buf[4] = 0xC3D2E1F0;

	for (int t = 0; t < size / (16 * 4); t++)//номер блока
	{
		// получаем очередные 512 бит сообщения (блок из 16 4-ех байтных слов)
		vector<unsigned long> x;
		x.resize(16);//делим 512 бит на 16 4-ех байтных слов
		for (int i = 0; i < 16; i++)//номер элемента в блоке
		{
			unsigned long mi = 0;//4-ех байтное переменное
			for (int k = 0; k < 4; k++)
			{
				mi |= AlignmentMsg[t * 16 * 4 + i * 4 + k] << k * 8;
			}
			x[i] = mi;
		}		

		unsigned long A1 = buf[0]; 
		unsigned long B1 = buf[1]; 
		unsigned long C1 = buf[2]; 
		unsigned long D1 = buf[3]; 
		unsigned long E1 = buf[4]; 

		unsigned long A2 = buf[0]; 
		unsigned long B2 = buf[1]; 
		unsigned long C2 = buf[2]; 
		unsigned long D2 = buf[3]; 
		unsigned long E2 = buf[4]; 

		unsigned long T;
		
		for (int j = 0; j < 80; j++)
		{
			T = cir_shift(A1 + f(j,B1,C1,D1) + x[R1[j]] + K1(j), S1[j]) + E1;
			A1 = E1; E1 = D1; D1 = cir_shift(C1, 10); C1 = B1; B1 = T;
			T = cir_shift(A2 + f(79-j, B2, C2, D2) + x[R2[j]] + K2(j), S2[j]) + E2;
			A2 = E2; E2 = D2; D2 = cir_shift(C2,10); C2 = B2; B2 = T;
		}

		T = buf[1] + C1 + D2; buf[1] = buf[2] + D1 + E2; buf[2] = buf[3] + E1 + A2;
		buf[3] = buf[4] + A1 +B2; buf[4] = buf[0] + B1 + C2; buf[0] = T;
	}

	ostringstream res;
	res.fill ('0'); //нулями будут «залиты» пустые позиции в результирующей строке
	for (int i = 0; i < 5; i++)
	{
		res << std::hex << inv(buf[i]);//setw(8) << inv(buf[i]);
		//соединяет в одну строку исходные значения слов дайджеста, который претерпел изменения, set(8) -указывает на мини-ую
		//ширину вывода одного дайджеста, то есть одному дайджесту уделяются 8 символов
	}

	char* result = new char[41];
	strcpy(result, (char*) res.str().c_str());
	return result;
}
bool WriteFile(char *fileName, string str)                                           
{
    ofstream out(fileName);                                                                 

    if (out.fail())                                                                         
        return false;                                                                       

    out << str;                                                                             

    return true;                                                                           
}

int main(int argc, char** argv)
{
	if (argc!=3)
	{
		cout<<"./RIPEMD_160 <InputFile><OutputFile>";
		return 1;
	}
	


//----------1-ый шаг алгоритма считать входной файл--------------------
	ifstream infile(argv[1], ios::binary); //входной поток
	
	if (infile.fail()) //если возникла ошибка                           
	{
		cout<<"Error in input!"<<endl;
        	return 1;
	}

	infile.seekg(0, ios::end); //считаем размер файла     
	int SizeOfFile = infile.tellg();
	infile.seekg(0, ios::beg);
	
	char* input = new char[SizeOfFile]();//создаем массив для хранения входного потока
	infile >> input;//копируем содержимое входного файла в массив 
	
	infile.close();
	//на выходе 1-ого шага имеем сообщение input
//----------------------------------------------------------------------------
	
	
//-----------2-ой шаг алгоритма Выравнивание входного потока------------------
	string in=input;//переводим сообщение в стринг, чтоб можно было пользоватся встроенными функциями типа string
	int length = in.length(); //пересчитываем размер сообщения без учета символа конца файла    
	
	int ostatok = length%64;//cчитаем байты в последнем блоке          
	
	int size = 0;//размер входного массива после выравнивания      

	if(ostatok < 56) //если есть свободных 8 байт, то не добавляем новый блок из 512 битов, а просто выравниваем до 512 бит
		size = length - ostatok + 56 + 8; 
	else  //если нету свободных 8 байт, то придется добавить новый блок, в котором будет 8 свободных байт           
		size = length + 64 - ostatok + 56 + 8;

	unsigned char *AlignmentMsg = new unsigned char[size];//cоздаем выровненный массив
	
	for(int i=0; i < length; i++) 
		AlignmentMsg[i] = in[i]; //копируем входной поток в выровненый массив
	
	AlignmentMsg[length] = 0x80;//после добавляем байт ввида 10000000
	
	for(int i = length + 1; i < size; i++)
		AlignmentMsg[i] = 0;//все остальное заполняем нулями	

	//теперь запишем в 8 резервных байтов вконце исходную длину входного потока 	
	int64_t bit_length = (unsigned int)(length)*8;	
	for(int i = 0; i < 8; i++)
		AlignmentMsg[size - 8 + i] = (unsigned char)(bit_length >> i * 8);
//--------------------------------------------------------------------------------
	

	WriteFile(argv[2],Ripemd(AlignmentMsg,size));
		


	return 0;
}




