#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test para el código proporcionado por el profesor
"""

from lexer import lexer
from parser import parser

codigo_profesor = """
#include stdio.h
    #define aktura 67.8

    int evaluar (int a, int b, float c){
    int p,q,*q, r=100, **u;
    float r;  
    char *z; 
    boolean val=true;
    //este es un comentario
    
    q=&p;
    if (a>0)
            p=a+1;
        else
            q=b;    ;
            if (b>0){
            p=1; 
                    while(p<=100){
                    q=q+1;
                    r--;
                    }
            }
            else{
                    for(p=0;p<100; p++){
                    c=c+1;
                    } 
    /* soy un comentario de varias lineas
        y no me creo mucho*/
                }
    a=b;
        
    switch(a)
    {
        case 1: a=b;
                break;
        case 2: a=c;
                break;
        case 3: c=a+b;
                break;
        default: a=0;
                break;      
            
            }
        
    return (a+1);              
    }

    int fibonaci(int i)
    {
    if(i == 0)
    {
        return 0;
    }
    if(i == 1)
    {
        return 1;
    }
    return fibonaci(i-1) + fibonaci(i-2);
    }
"""

if __name__ == '__main__':
    print("=" * 80)
    print("COMPILADOR - TEST CON CÓDIGO DEL PROFESOR")
    print("=" * 80)
    print("\n--- CÓDIGO FUENTE ---")
    print(codigo_profesor)
    
    print("\n--- ANÁLISIS LÉXICO ---")
    lexer.input(codigo_profesor)
    print("Tokens reconocidos:")
    for tok in lexer:
        print(f"  {tok.type}: {tok.value}")
    
    print("\n--- ANÁLISIS SINTÁCTICO Y SEMÁNTICO ---")
    try:
        result = parser.parse(codigo_profesor, lexer=lexer)
        print("\n✓ COMPILACIÓN EXITOSA")
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
    
    print("\n" + "=" * 80)
