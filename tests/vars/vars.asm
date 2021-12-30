BITS 64
;; Subroutine to print an integer
;; in the rax register
_printRAX:
	mov rcx, digitSpace
	mov rbx, 10
	mov [rcx], rbx
	inc rcx
	mov [digitSpacePos], rcx

_printRAXLoop:
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
	jne _printRAXLoop

_printRAXLoop2:
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
	jge _printRAXLoop2

	ret



section .bss
    digitSpace resb 100
    digitSpacePos resb 8
    memory resb 800

section .text
    global _start:

_start:
_addr0:
    ;; PUSH 69 ;;
    push 69

_addr1:
    ;; PUSH 420 ;;
    push 420

_addr2:
    ;; POP:myvar
    pop rax
    mov [memory+1], rax
_addr3:
    ;; PUSH 3 ;;
    push 3

_addr4:
    ;; PUSH 5 ;;
    push 5

_addr5:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr6:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
