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

section .text
    global _start:

_start:
_addr0:
    ;; PUSH 69 ;;
    push 69

_addr1:
    ;; while ;; 
    mov rax, [rsp]
    test rax, rax
    jz _addr7
_addr2:
    pop rax
    push rax
    push rax
_addr3:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr4:
    ;; PUSH 1 ;;
    push 1

_addr5:
    ;; SUB ;;
    pop rax
    pop rbx
    sub rbx, rax
    push rbx

_addr6:
    ;; end ;;
    jmp _addr1
_addr7:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
