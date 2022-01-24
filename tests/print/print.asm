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
    ;; PUSH 1 ;;
    push 1

_addr1:
    ;; PUSH 2 ;;
    push 2

_addr2:
    ;; PUSH 3 ;;
    push 3

_addr3:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr4:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr5:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr6:
    ;; PUSH 1 ;;
    push 1

_addr7:
    ;; PUSH 2 ;;
    push 2

_addr8:
    ;; PUSH 3 ;;
    push 3

_addr9:
    ;; PRINT ;;
    pop rax
    call _printRAXNoNewLine

_addr10:
    ;; PRINT ;;
    pop rax
    call _printRAXNoNewLine

_addr11:
    ;; PRINT ;;
    pop rax
    call _printRAXNoNewLine

_addr12:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
