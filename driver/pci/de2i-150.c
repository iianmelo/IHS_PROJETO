#include <linux/init.h> 	//Contém as macros de inicialização do kernel.
#include <linux/module.h>	/* THIS_MODULE macro - Fornece as macros essenciais para a definição de módulos do kernel.*/
#include <linux/fs.h>		/* VFS related - Contém as estruturas e funções relacionadas ao subsistema de sistema de arquivos.*/
#include <linux/ioctl.h>	/* ioctl syscall - Define as constantes para o uso da syscall ioctl.*/
#include <linux/errno.h>	/* error codes - Define os códigos de erro padrão do kernel.*/
#include <linux/types.h>	/* dev_t number - Define tipos de dados comuns do kernel.*/
#include <linux/cdev.h>		/* char device registration - Fornece as estruturas e funções necessárias para registrar um dispositivo de caractere no kernel.*/
#include <linux/uaccess.h>	/* copy_*_user functions - Contém as funções para copiar dados entre o espaço do usuário e o espaço do kernel de forma segura.*/
#include <linux/pci.h>		/* pci funcs and types - Fornece estruturas e funções relacionadas à comunicação com dispositivos PCI.*/

#include "../../include/ioctl_cmds.h"

/* meta information */

MODULE_LICENSE("GPL"); //Define a licença do módulo como GPL.
MODULE_AUTHOR("mfbsouza"); //Define o autor do módulo.
MODULE_DESCRIPTION("simple pci driver for DE2i-150 dev board"); //Descreve o propósito do módulo.

/* driver constants */
//Nome do driver.
#define DRIVER_NAME      "my_driver" 
//Nome do dispositivo de caractere associado ao driver.
#define FILE_NAME        "mydev" 
 //Classe do driver.
#define DRIVER_CLASS     "MyModuleClass"
//ID do fornecedor do dispositivo PCI.
#define MY_PCI_VENDOR_ID  0x1172 
//ID do dispositivo PCI.
#define MY_PCI_DEVICE_ID  0x0004 

/* lkm entry and exit functions */

static int  __init my_init (void); // Função de inicialização do módulo.
static void __exit my_exit (void); // Função de saída do módulo.

/* char device system calls */

static int	my_open   (struct inode*, struct file*); //Geralmente, é usada para inicializar o estado do dispositivo ou reservar recursos associados a ele.
static int 	my_close  (struct inode*, struct file*); //É usada para limpar e liberar os recursos associados ao dispositivo que foram alocados durante a abertura.
static ssize_t 	my_read   (struct file*, char __user*, size_t, loff_t*); //responsável por ler os dados do dispositivo e copiá-los para o espaço de usuário.
static ssize_t 	my_write  (struct file*, const char __user*, size_t, loff_t*); //responsável por receber os dados do espaço de usuário e escrevê-los no dispositivo.
static long int	my_ioctl  (struct file*, unsigned int, unsigned long); // As chamadas ioctl são usadas para operações específicas do dispositivo que não se enquadram nas operações de leitura e gravação padrão.

/* pci functions */

static int  __init my_pci_probe  (struct pci_dev *dev, const struct pci_device_id *id);
static void __exit my_pci_remove (struct pci_dev *dev);

/* pci ids which this driver supports */

//Contém um único elemento que especifica o par de identificadores de fornecedor e dispositivo PCI suportados pelo driver.
static struct pci_device_id pci_ids[] = {
	{PCI_DEVICE(MY_PCI_VENDOR_ID, MY_PCI_DEVICE_ID), },
	{0, }
};
MODULE_DEVICE_TABLE(pci, pci_ids); //Esta macro declara a tabela de dispositivos do módulo, o que permite que o kernel saiba quais dispositivos este módulo de driver pode lidar.

/* device file operations */

// define as operações que podem ser realizadas no dispositivo.(ponteiros)
static struct file_operations fops = {
	.owner = THIS_MODULE,
	.read = my_read,
	.write = my_write,
	.unlocked_ioctl	= my_ioctl,
	.open = my_open,
	.release = my_close
};

/* pci driver operations */

//Esta estrutura representa o driver PCI. 
static struct pci_driver pci_ops = {
	.name = DRIVER_NAME,
	.id_table = pci_ids,
	.probe = my_pci_probe,
	.remove = my_pci_remove
};

/* variables for char device registration to kernel */

static dev_t my_device_nbr; //Armazena o número de dispositivo alocado pelo kernel.
static struct class* my_class; //Representa a classe de dispositivo criada.
static struct cdev my_device; //Representa o dispositivo de caractere que está sendo registrado.

/* --- device data --- */
/* PCI BARs mapped to virtual space */
static void __iomem* bar0_mmio = NULL;

/* MMIO pointers used in write() read() ioctl() */
static void __iomem* read_pointer  = NULL;
static void __iomem* write_pointer = NULL;

/* peripherals names for debugging in dmesg */
static const char* peripheral[] = {
	"switches",
	"p_buttons",
	"display_l",
	"display_r",
	"green_leds",
	"red_leds"
};

enum perf_names_idx {
	IDX_SWITCH = 0,
	IDX_PBUTTONS,
	IDX_DISPLAYL,
	IDX_DISPLAYR,
	IDX_GREENLED,
	IDX_REDLED
};
static int wr_name_idx = IDX_DISPLAYR;
static int rd_name_idx = IDX_SWITCH;

/* functions implementation */

static int __init my_init(void)
{
	printk("my_driver: loaded to the kernel\n");

	/* 0. register pci driver to the kernel */
	if (pci_register_driver(&pci_ops) < 0) {
		printk("my_driver: PCI driver registration failed\n");
		return -EAGAIN;
	}

	/* 1. request the kernel for a device number */
	if (alloc_chrdev_region(&my_device_nbr, 0, 1, DRIVER_NAME) < 0) {
		printk("my_driver: device number could not be allocated!\n");
		return -EAGAIN;
	}
	printk("my_driver: device number %d was registered!\n", MAJOR(my_device_nbr));

	/* 2. create class : appears at /sys/class */
	if ((my_class = class_create(THIS_MODULE, DRIVER_CLASS)) == NULL) {
		printk("my_driver: device class count not be created!\n");
		goto ClassError;
	}

	/* 3. associate the cdev with a set of file operations */
	cdev_init(&my_device, &fops);

	/* 4. create the device node */
	if (device_create(my_class, NULL, my_device_nbr, NULL, FILE_NAME) == NULL) {
		printk("my_driver: can not create device file!\n");
		goto FileError;
	}

	/* 5. now make the device live for the users to access */
	if (cdev_add(&my_device, my_device_nbr, 1) == -1){
		printk("my_driver: registering of device to kernel failed!\n");
		goto AddError;
	}

	return 0;

AddError:
	device_destroy(my_class, my_device_nbr);
FileError:
	class_destroy(my_class);
ClassError:
	unregister_chrdev(my_device_nbr, DRIVER_NAME);
	pci_unregister_driver(&pci_ops);
	return -EAGAIN;
}

static void __exit my_exit(void)
{
	cdev_del(&my_device);
	device_destroy(my_class, my_device_nbr);
	class_destroy(my_class);
	unregister_chrdev(my_device_nbr, DRIVER_NAME);
	pci_unregister_driver(&pci_ops);
	printk("my_driver: goodbye kernel!\n");
}

static int my_open(struct inode* inode, struct file* filp)
{
	printk("my_driver: open was called\n");
	return 0;
}

static int my_close(struct inode* inode, struct file* filp)
{
	printk("my_driver: close was called\n");
	return 0;
}

static ssize_t my_read(struct file* filp, char __user* buf, size_t count, loff_t* f_pos)
{
	ssize_t retval = 0;
	int to_cpy = 0;
	static unsigned int temp_read = 0;

	/* check if the read_pointer pointer is set */
	if (read_pointer == NULL) {
		printk("my_driver: trying to read to a device region not set yet\n");
		return -ECANCELED;
	}

	/* read from the device */
	temp_read = ioread32(read_pointer);
	printk("my_driver: red 0x%X from the %s\n", temp_read, peripheral[rd_name_idx]);

	/* get amount of bytes to copy to user */
	to_cpy = (count <= sizeof(temp_read)) ? count : sizeof(temp_read);

	/* copy data to user */
	retval = to_cpy - copy_to_user(buf, &temp_read, to_cpy);

	return retval;
}

static ssize_t my_write(struct file* filp, const char __user* buf, size_t count, loff_t* f_pos)
{
	ssize_t retval = 0;
	int to_cpy = 0;
	static unsigned int temp_write = 0;

	/* check if the write_pointer pointer is set */
	if (write_pointer == NULL) {
		printk("my_driver: trying to write to a device region not set yet\n");
		return -ECANCELED;
	}

	/* get amount of bytes to copy from user */
	to_cpy = (count <= sizeof(temp_write)) ? count : sizeof(temp_write);

	/* copy data from user */
	retval = to_cpy - copy_from_user(&temp_write, buf, to_cpy);

	/* send to device */
	iowrite32(temp_write, write_pointer);
	printk("my_writer: wrote 0x%X to the %s\n", temp_write, peripheral[wr_name_idx]);

	return retval;
}

static long int my_ioctl(struct file*, unsigned int cmd, unsigned long arg)
{
	switch(cmd){
	case RD_SWITCHES:
		read_pointer = bar0_mmio + 0xC020; //TODO: update offset
		rd_name_idx = IDX_SWITCH;
		break;
	case RD_PBUTTONS:
		read_pointer = bar0_mmio + 0xC060; //TODO: update offset
		rd_name_idx = IDX_PBUTTONS;
		break;
	case WR_L_DISPLAY:
		write_pointer = bar0_mmio + 0xC040; //TODO: update offset
		wr_name_idx = IDX_DISPLAYL;
		break;
	case WR_R_DISPLAY:
		write_pointer = bar0_mmio + 0xC000; //TODO: update offset
		wr_name_idx = IDX_DISPLAYR;
		break;
	case WR_RED_LEDS:
		write_pointer = bar0_mmio + 0xC080; //TODO: update offset
		wr_name_idx = IDX_DISPLAYR;
		break;
	case WR_GREEN_LEDS:
		write_pointer = bar0_mmio + 0xC100; //TODO: update offset
		wr_name_idx = IDX_DISPLAYR;
		break;
	default:
		printk("my_driver: unknown ioctl command: 0x%X\n", cmd);
	}
	return 0;
}

static int __init my_pci_probe(struct pci_dev *dev, const struct pci_device_id *id)
{
	unsigned short vendor, device;
	unsigned char rev;
	unsigned int bar_value;
	unsigned long bar_len;

	/* enable the device */
	if (pci_enable_device(dev) < 0) {
		printk("my_driver: Could not enable the PCI device!\n");
		return -EBUSY;
	}
	printk("my_driver: PCI device enabled\n");

	/* read some info from the PCI configuration space */
	pci_read_config_word(dev, PCI_VENDOR_ID, &vendor);
	pci_read_config_word(dev, PCI_DEVICE_ID, &device);
	pci_read_config_byte(dev, PCI_REVISION_ID, &rev);
	printk("my_driver: PCI device - Vendor 0x%X Device 0x%X Rev 0x%X\n", vendor, device, rev);

	/* read info about the PCI device BAR0 */
	pci_read_config_dword(dev, 0x10, &bar_value);
	bar_len = pci_resource_len(dev, 0);
	printk("my_driver: PCI device - BAR0 => 0x%X with length of %ld Kbytes\n", bar_value, bar_len/1024);

	/* mark the PCI BAR0 region as reserved to this driver */
	if (pci_request_region(dev, 0, DRIVER_NAME) != 0) {
		printk("my_driver: PCI Error - PCI BAR0 region already in use!\n");
		pci_disable_device(dev);
		return -EBUSY;
	}

	/* map the BAR0 Physical address space to virtual space */
	bar0_mmio = pci_iomap(dev, 0, bar_len);

	/* initialize a default peripheral read and write pointer */
	write_pointer = bar0_mmio + 0xC000; //TODO: update offset
	read_pointer  = bar0_mmio + 0xC080; //TODO: update offset

	return 0;
}

static void __exit my_pci_remove(struct pci_dev *dev)
{
	read_pointer = NULL;
	write_pointer = NULL;

	/* remove the IO mapping done in probe func */
	pci_iounmap(dev, bar0_mmio);

	/* disable the PCI device */
	pci_disable_device(dev);

	/* unmark device PCI BAR0 as reserved */
	pci_release_region(dev, 0);

	printk("my_driver: PCI Device - Disabled and BAR0 Released");
}

module_init(my_init);
module_exit(my_exit);
