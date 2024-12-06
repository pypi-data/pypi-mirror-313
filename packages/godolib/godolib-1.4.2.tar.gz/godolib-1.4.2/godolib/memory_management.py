import psutil
import os
import pynvml

def memory_usage():
    """
    Imprime la cantidad de memoria RAM utilizada por el proceso actual en megabytes (MB).

    Esta función utiliza la biblioteca `psutil` para acceder a la información del sistema, 
    específicamente al uso de memoria del proceso que está ejecutando el código. La memoria 
    utilizada se mide en bytes y se convierte a megabytes para una mejor legibilidad.

    Ejemplo:
        >>> obtener_uso_memoria()
        Uso de memoria: 120.35 MB
    """
    proceso = psutil.Process(os.getpid())
    memoria_en_mb = proceso.memory_info().rss / (1024 * 1024)
    print(f"Used Memory: {memoria_en_mb:.2f} MB")

def gpu_memory(gpu_indices, display=True, units="MB"):
    """
    Retrieves memory usage details for specified GPUs.

    Args:
        gpu_indices (list): List of GPU indices to query (e.g., [0, 1, 2]).
        display (bool): If True, prints the memory details. Default is True.
        units (str): Unit of measurement for memory. Options: "MB", "GB", "KB". Default is "MB".

    Returns:
        dict: A dictionary where each GPU index maps to another dictionary 
              containing 'total', 'used', and 'free' memory in the specified units.

    Example:
        >>> gpu_memory([0, 1], display=True, units="GB")
        GPU 0:
          Total Memory: 16.00 GB
          Used Memory: 2.00 GB
          Free Memory: 14.00 GB
        GPU 1:
          Total Memory: 8.00 GB
          Used Memory: 1.00 GB
          Free Memory: 7.00 GB
        {'GPU 0': {'total': 16.00, 'used': 2.00, 'free': 14.00},
         'GPU 1': {'total': 8.00, 'used': 1.00, 'free': 7.00}}
    """
    # Conversion factors for different units
    conversion_factors = {"MB": 1024 ** 2, "GB": 1024 ** 3, "KB": 1024}
    if units not in conversion_factors:
        raise ValueError(f"Unsupported unit: {units}. Choose from 'MB', 'GB', or 'KB'.")
    
    factor = conversion_factors[units]
    memory_details = {}

    if isinstance (gpu_indices, int):
        gpu_indices=[gpu_indices]

    try:
        # Initialize NVML
        pynvml.nvmlInit()

        for index in gpu_indices:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(index)
                info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                # Convert memory values to the specified units
                memory_info = {
                    "total": info.total / factor,
                    "used": info.used / factor,
                    "free": info.free / factor
                }
                memory_details[f"{index}"] = memory_info
                
                # Optionally display the details
                if display:
                    print(f"GPU {index}:")
                    print(f"  Total Memory: {memory_info['total']:.2f} {units}")
                    print(f"  Used Memory: {memory_info['used']:.2f} {units}")
                    print(f"  Free Memory: {memory_info['free']:.2f} {units}")
            except pynvml.NVMLError as e:
                print(f"Error accessing GPU {index}: {e}")

    except pynvml.NVMLError as e:
        print(f"Error initializing NVML: {e}")
    finally:
        # Shutdown NVML
        pynvml.nvmlShutdown()
    
    return memory_details
