BITS 64
_printRAX:
	mov rcx, digitSpace2
	mov rbx, 10
	mov [rcx], rbx
	inc rcx
	mov [digitSpacePos2], rcx

_printRAXLoop:
	mov rdx, 0
	mov rbx, 10
	div rbx
	push rax
	add rdx, 48

	mov rcx, [digitSpacePos2]
	mov [rcx], dl
	inc rcx
	mov [digitSpacePos2], rcx

	pop rax
	cmp rax, 0
	jne _printRAXLoop

_printRAXLoop2:
	mov rcx, [digitSpacePos2]

	mov rax, 1
	mov rdi, 1
	mov rsi, rcx
	mov rdx, 1
	syscall

	mov rcx, [digitSpacePos2]
	dec rcx
	mov [digitSpacePos2], rcx

	cmp rcx, digitSpace2
	jge _printRAXLoop2

	ret
_printRAXNoNewLine:
	mov rcx, digitSpace
	;mov rbx, 10
	;mov [rcx], rbx
	inc rcx
	mov [digitSpacePos], rcx

_printRAXNoNewLineLoop:
	mov rdx, 0
	mov rbx, 10
	div rbx
	push rax
	add rdx, 48

	mov rcx, [digitSpacePos]
	mov [rcx], dl
	inc rcx
	mov [digitSpacePos], rcx

	pop rax
	cmp rax, 0
	jne _printRAXNoNewLineLoop

_printRAXNoNewLineLoop2:
	mov rcx, [digitSpacePos]

	mov rax, 1
	mov rdi, 1
	mov rsi, rcx
	mov rdx, 1
	syscall

	mov rcx, [digitSpacePos]
	dec rcx
	mov [digitSpacePos], rcx

	cmp rcx, digitSpace
	jge _printRAXNoNewLineLoop2

	ret



_square:
    add r10, 8
    pop r14
    mov [returnstack+r10], r14
_addr1:
    pop rax
    push rax
    push rax
_addr2:
    ;; MULTIPLY ;;
    pop rax
    pop rbx
    imul rbx
    push rax

_addr3:
mov r14, [returnstack+r10]
push r14
sub r10, 8
ret
section .data

section .bss
    digitSpace resb 100
    digitSpacePos resb 8
    digitSpace2 resb 100
    digitSpacePos2 resb 8
    memory resb 800

    returnstack resb 800

section .text
    global _start:

_start:
    mov r10, -1
_addr0:
_addr4:
    ;; PUSH 6 ;;
    push 6

_addr5:
call _square
_addr6:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr7:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
