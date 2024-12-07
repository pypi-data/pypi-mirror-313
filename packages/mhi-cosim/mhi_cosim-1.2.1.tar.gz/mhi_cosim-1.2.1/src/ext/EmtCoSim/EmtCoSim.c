/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/
/* EmtCosim.c                                                                     */
/*--------------------------------------------------------------------------------*/
/*                                                                                */
/* This is the open-source implementation of the interface into the PSCAD         */
/* Communication Fabric. This code will automatically Construct and Multiplex     */
/* all communication between itself and PSCAD, or a running EMTDC instance.       */
/*                                                                                */
/* This is to be used for Co-Simulation of PSCAD/EMTDC with other applications    */
/*                                                                                */
/* Created By:                                                                    */
/* ~~~~~~~~~~~                                                                    */
/*   PSCAD Design Group <pscad@hvdc.ca>                                           */
/*   Manitoba HVDC Research Centre                                                */
/*   Winnipeg, Manitoba. CANADA                                                   */
/*                                                                                */
/*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*/

/* Public Definition Header */
#include "EmtCoSim.h"

/* Dependencies */
#include <Windows.h>          /* Used For System Calls                          */
#include <stdint.h>           /* Used For accessing specific byte count values  */
#include <assert.h>           /* Debugging asserts                              */
#include <stdio.h>            /* Used for file reading                          */
#include <float.h>            /* Used for max double                            */

#ifndef POSIX
#define strcmpi  _strcmpi           /* For POSIX Compatibility */
#define strnicmp _strnicmp
#endif

/*==============================================================================*/
/* EmtdcCosimulation_Channel                                                    */
/*------------------------------------------------------------------------------*/
/* The manager for a specific channel of information traveling between this     */
/* Client and another client, the channel should be globally unique across the  */
/* entire system                                                                */
/*==============================================================================*/

struct EmtdcCosimulation_Channel_S;
typedef struct EmtdcCosimulation_Channel_S EmtdcCosimulation_Channel;

/*==============================================================================*/
/* ChannelImpl                                                                  */
/*------------------------------------------------------------------------------*/
/* This is the internal representation of the Channel, The                      */
/* EmtdcCosimulation_Channel is a thin wrapper for this structure               */
/*==============================================================================*/

struct EmtdcCosimulation_Channel_Impl_S;
typedef struct EmtdcCosimulation_Channel_Impl_S ChannelImpl;

/*==============================================================================*/
/* HashTable                                                                    */
/*------------------------------------------------------------------------------*/
/* This is a fast hash-table used to quickly retrieve objects by a hash         */
/* identifier                                                                   */
/*==============================================================================*/

struct EmtdcCosimulation_HashTable_S;
struct EmtdcCosimulation_HashTable_Entry_S;

typedef struct EmtdcCosimulation_HashTable_S          HashTable;
typedef struct EmtdcCosimulation_HashTable_Entry_S    HashTableEntry;
typedef void*                                         HashTableObject;

/*==============================================================================*/
/* Message                                                                      */
/*------------------------------------------------------------------------------*/
/* This is a fast hash-table used to quickly retrieve objects by a hash         */
/* identifier                                                                   */
/*                                                                              */
/* This is a node in a linked list of received messages                         */
/*==============================================================================*/

struct EmtdcCosimulation_Message_S;
typedef struct EmtdcCosimulation_Message_S Message;

/*==============================================================================*/
/* Buffer                                                                       */
/*------------------------------------------------------------------------------*/
/* Maintains the life of an arbitrary sized data buffer                         */
/*==============================================================================*/

struct EmtdcCosimulation_Buffer_S;
typedef struct EmtdcCosimulation_Buffer_S Buffer;

/*==============================================================================*/
/* Initialization Data                                                          */
/*------------------------------------------------------------------------------*/
/* The data for initializing the co-simulation                                  */
/*==============================================================================*/

struct EmtdcCosimulation_InitData_S;
typedef struct EmtdcCosimulation_InitData_S InitData;

/*==============================================================================*/
/* Singletons                                                                   */
/*------------------------------------------------------------------------------*/
/* These can, and should be only accessible to the local file.                  */
/*==============================================================================*/

static HashTable *      pEmtdcCosimulation_ChannelManager = NULL;
static char             sEmtdcCosimulation_HostName[256];
static int              iEmtdcCosimulation_Port = -1;
static unsigned short   iEmtdcCosimulation_ClientId = 0;
static double           dEmtdcCosimulation_Time = 0.0;
static double           dEmtdcCosimulation_Step = 0.0;

/*==============================================================================*/
/* EmtdcCosimulation_Channel                                                    */
/*------------------------------------------------------------------------------*/
/* The manager for a specific channel of information traveling between this     */
/* Client and another client, the channel should be globally unique across the  */
/* entire system                                                                */
/*==============================================================================*/

/*===================================================================*/
/* Constructor / Destructor                                          */
/*===================================================================*/
static EmtdcCosimulation_Channel * EmtdcCosimulation_Channel_Create(unsigned short client_id, unsigned int channel_id, int recv_size, int send_size);
static void           EmtdcCosimulation_Channel_Delete(EmtdcCosimulation_Channel* _this);

/*-------------------------------------------------------------------*/
/* Member Functions                                                  */
/*-------------------------------------------------------------------*/
static double       EmtdcCosimulation_Channel_GetValue        (EmtdcCosimulation_Channel* _this, double time, int index);
static void         EmtdcCosimulation_Channel_SetValue        (EmtdcCosimulation_Channel* _this, double val, int index);
static void         EmtdcCosimulation_Channel_Send            (EmtdcCosimulation_Channel* _this, double time);
static unsigned int EmtdcCosimulation_Channel_GetChannelId    (EmtdcCosimulation_Channel* _this);
static int          EmtdcCosimulation_Channel_GetSendSize     (EmtdcCosimulation_Channel* _this);
static int          EmtdcCosimulation_Channel_GetRecvSize     (EmtdcCosimulation_Channel* _this);

/*==============================================================================*/
/* ChannelImpl                                                                  */
/*------------------------------------------------------------------------------*/
/* This is the internal representation of the Channel, The                      */
/* EmtdcCosimulation_Channel is a thin wrapper for this structure               */
/*==============================================================================*/

/*-------------------------------------------------------------------*/
/* Shared Members                                                    */
/*-------------------------------------------------------------------*/
static Buffer *     pEmtdcCosimulation_Channel_Impl_Buffer = NULL;
static int          iEmtdcCosimulation_Channel_Impl_Master = 0;

/*-------------------------------------------------------------------*/
/* Shared Functions                                                  */
/*-------------------------------------------------------------------*/
static unsigned int   EmtdcCosimulation_Channel_Impl_GetNextChannelMessage(unsigned short client_id);

/*===================================================================*/
/* Constructor / Destructor                                          */
/*===================================================================*/
static ChannelImpl * EmtdcCosimulation_Channel_Impl_Create(unsigned short client_id, unsigned int channel_id, int recv_size, int send_size);
static void          EmtdcCosimulation_Channel_Impl_Delete(ChannelImpl* _this);

/*-------------------------------------------------------------------*/
/* Member Functions                                                  */
/*-------------------------------------------------------------------*/
static double         EmtdcCosimulation_Channel_Impl_GetValue        (ChannelImpl* _this, double time, int i);
static void           EmtdcCosimulation_Channel_Impl_SetValue        (ChannelImpl* _this, double d, int i);
static void           EmtdcCosimulation_Channel_Impl_Send            (ChannelImpl* _this, double time);
static void           EmtdcCosimulation_Channel_Impl_Parse           (ChannelImpl* _this, void * ptr, int size);
static char *         EmtdcCosimulation_Channel_Impl_SetValueBufferI (ChannelImpl* _this, char* ptr, unsigned int val);
static char *         EmtdcCosimulation_Channel_Impl_SetValueBufferD (ChannelImpl* _this, char* ptr, double val);
static void           EmtdcCosimulation_Channel_Impl_Send_Final      (ChannelImpl* _this);

/*-------------------------------------------------------------------*/
/* Structure                                                         */
/*-------------------------------------------------------------------*/
struct EmtdcCosimulation_Channel_Impl_S
   {
   unsigned short    iClientId;           /* The Client ID of the foreign Client that this channel is connected to */
   unsigned int      iChannelId;          /* A System wide unique value used to identify this information channel  */
   int               iRecvSize;           /* The size of the data being received                                   */
   int               iSendSize;           /* The size of the data being sent                                       */
   unsigned short    iMessageSize;        /* A cache of the complete message size                                  */

   Message *         pLastMessage;
   Message *         pSendMessage;        /* The message being constructed to send                                 */
   Message *         pRecvMessage;        /* The currently received message (list)                                 */
   Message *         pRecvMessageBuffer;  /* A backlog, of allocated messages that can be overwritten              */
   };

/*==============================================================================*/
/* Primitive Marshalling                                                        */
/*------------------------------------------------------------------------------*/
/* The following function are created to perform Bit-wise Marshalling           */
/* on primitive types to pass information quickly and robustly over             */
/* an unknown connection                                                        */
/*==============================================================================*/

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Marshal_int32()                                 */
/*-------------------------------------------------------------------*/
static int32_t  EmtdcCosimulation_Marshal_int32  (int32_t value)
   {
   unsigned char bytes[sizeof(int32_t)];
   int i;
   for(i=0; i<sizeof(int32_t); i++)
      bytes[i]=(unsigned char)(value>>(8*(sizeof(int32_t)-i-1)));
   return *((int32_t*)bytes);
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Marshal_int64()                                 */
/*-------------------------------------------------------------------*/
static int64_t  EmtdcCosimulation_Marshal_int64  (int64_t value)
   {
   unsigned char bytes[sizeof(int64_t)];
   int i;
   for(i=0; i<sizeof(int64_t); i++)
      bytes[i]=(unsigned char)(value>>(8*(sizeof(int64_t)-i-1)));
   return *((int64_t*)bytes);
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Marshal_double()                                */
/*-------------------------------------------------------------------*/
static double EmtdcCosimulation_Marshal_double(double value)
   {
   uint64_t a;
   a = EmtdcCosimulation_Marshal_int64(*((uint64_t*)(&value)));
   return *((double*)(&a));
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Extract_int32()                                 */
/*-------------------------------------------------------------------*/
static void * EmtdcCosimulation_Extract_int32(void * ptr, uint32_t * value)
   {
   (*value) = EmtdcCosimulation_Marshal_int32(*(uint32_t*)(ptr));
   return (char*)ptr + sizeof(uint32_t);
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Extract_double()                                */
/*-------------------------------------------------------------------*/
static void * EmtdcCosimulation_Extract_double(void * ptr, double  * value)
   {
   (*value) = EmtdcCosimulation_Marshal_double(*(double*)(ptr));
   return (char*)ptr + sizeof(double);
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Insert_Int32()                                  */
/*-------------------------------------------------------------------*/
static void * EmtdcCosimulation_Insert_int32(void * ptr, int32_t value)
   {
   *((int32_t*)(ptr)) = EmtdcCosimulation_Marshal_int32(value);
   return (char*)ptr + sizeof(int32_t);
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_Insert_String()                                 */
/*-------------------------------------------------------------------*/
static void * EmtdcCosimulation_Insert_string(void * ptr, char * value)
   {
   int len;
   len = (int)strlen(value);
   memcpy(ptr, value, len + 1);
   return (char*)ptr + len + 1;
   }

/*-------------------------------------------------------------------*/
/* EmtdcCosimulation_string_trim()                                   */
/*-------------------------------------------------------------------*/
static char* EmtdcCosimulation_string_trim(char * str)
   {
   char *end;

   /* Trim leading space  */
   /**/
   while (isspace(*str))
      str++;

   /* If empty string */
   if (*str == 0)
      return str;

   /* Trim trailing space */
   /**/
   end = str + strlen(str) - 1;
   while (end > str && isspace(*end))
      end--;

   /* Write new null terminator character */
   /**/
   end[1] = '\0';

   return str;
   }

/*==============================================================================*/
/* CommunicationFabric                                                          */
/*------------------------------------------------------------------------------*/
/* This namespace contains the calls into the Communication Fabric DLL.         */
/*==============================================================================*/

#define NONBLOCKING 0x0001

/*-------------------------------------------------------------------*/
/* Types                                                             */
/*-------------------------------------------------------------------*/
typedef int (_cdecl * CommunicationFabric_Init_Func)(int argc, char * args[]);
typedef int (_cdecl * CommunicationFabric_Com_Func)(unsigned short to, void * buffer, unsigned short size, unsigned short flag);

/*-------------------------------------------------------------------*/
/* Variables                                                         */
/*-------------------------------------------------------------------*/
static HMODULE hComFabLibrary = NULL;         /* Handle to Library */
static CommunicationFabric_Init_Func   _CommunicationFabric_Initialize   = NULL;  /* Function Pointer to the Communication Fabric Initialize  function */
static CommunicationFabric_Init_Func   _CommunicationFabric_Finalize     = NULL;  /* Function Pointer to the Communication Fabric Finalize    function */
static CommunicationFabric_Com_Func    _CommunicationFabric_Send_Client  = NULL;  /* Function Pointer to the Communication Fabric send_client function */
static CommunicationFabric_Com_Func    _CommunicationFabric_Recv_Client  = NULL;  /* Function Pointer to the Communication Fabric recv_client function */
static CommunicationFabric_Com_Func    _CommunicationFabric_Peek_Client  = NULL;  /* Function Pointer to the Communication Fabric peek_client function */
static CommunicationFabric_Com_Func    _CommunicationFabric_Send_Server  = NULL;  /* Function Pointer to the Communication Fabric send_server function */
static CommunicationFabric_Com_Func    _CommunicationFabric_Recv_Server  = NULL;  /* Function Pointer to the Communication Fabric recv_server function */
static CommunicationFabric_Com_Func    _CommunicationFabric_Peek_Server  = NULL;  /* Function Pointer to the Communication Fabric peek_server function */

/*-------------------------------------------------------------------*/
/* Functions                                                         */
/*-------------------------------------------------------------------*/

/* Loads the Communication Fabric and finds the required Function pointers */
static int CommunicationFabric_Load(const char * location);
static int CommunicationFabric_Unload();

/* Call into the Communication Fabric */
static int CommunicationFabric_Initialize(int argc, char * args[]);
static int CommunicationFabric_Finalize(int argc, char * args[]);
static int CommunicationFabric_Send_Client(unsigned short to, void * buffer, unsigned short size, unsigned short flag);
static int CommunicationFabric_Recv_Client(unsigned short to, void * buffer, unsigned short size, unsigned short flag);
static int CommunicationFabric_Peek_Client(unsigned short to, void * buffer, unsigned short size, unsigned short flag);
static int CommunicationFabric_Send_Server(unsigned short to, void * buffer, unsigned short size, unsigned short flag);
static int CommunicationFabric_Recv_Server(unsigned short to, void * buffer, unsigned short size, unsigned short flag);
static int CommunicationFabric_Peek_Server(unsigned short to, void * buffer, unsigned short size, unsigned short flag);

/*==============================================================================*/
/* HashTable                                                                    */
/*------------------------------------------------------------------------------*/
/* This is a fast hash-table used to quickly retrieve objects by a hash         */
/* identifier                                                                   */
/*==============================================================================*/

/*-------------------------------------------------------------------*/
/* Constants                                                         */
/*-------------------------------------------------------------------*/

static const int  iEmtdcCosimulation_HashTable_StartSize        = 32;
static const int  iEmtdcCosimulation_HashTable_StartCapacity    = 16;
static const int  iEmtdcCosimulation_HashTable_HashMulti        = 7;
static const int  iEmtdcCosimulation_HashTable_EmptyDivisor     = 4;
static const int  iEmtdcCosimulation_HashTable_EmptyMin         = 10;

/*===================================================================*/
/* Constructor / Destructor                                          */
/*===================================================================*/
static HashTable * EmtdcCosimulation_HashTable_Create(double fill_cap);
static void EmtdcCosimulation_HashTable_Delete(HashTable * _this);

/*-------------------------------------------------------------------*/
/* Member Functions                                                  */
/*-------------------------------------------------------------------*/
static void*  EmtdcCosimulation_HashTable_Fetch(HashTable * _this, int key);
static int    EmtdcCosimulation_HashTable_Append(HashTable * _this, void* object, int key);
static int    EmtdcCosimulation_HashTable_Remove(HashTable * _this, int key);
static int    EmtdcCosimulation_HashTable_GetCount(HashTable * _this);
static int    EmtdcCosimulation_HashTable_GetKey(HashTable * _this, int index) ;
static void*  EmtdcCosimulation_HashTable_Get(HashTable * _this, int index);
static void   EmtdcCosimulation_HashTable_EnsureCapacity(HashTable * _this, int size);
static int    EmtdcCosimulation_HashTable_Hash(HashTable * _this, int val, int is_new, HashTableEntry* entries, int size);
static void   EmtdcCosimulation_HashTable_Rebuild(HashTable * _this, int capacity);

/*-------------------------------------------------------------------*/
/* Sub Structure                                                     */
/*-------------------------------------------------------------------*/
struct EmtdcCosimulation_HashTable_Entry_S
   {
   int iKey;
   int iIndex;
   };

/*-------------------------------------------------------------------*/
/* Structure                                                         */
/*-------------------------------------------------------------------*/
struct EmtdcCosimulation_HashTable_S
   {
   int      *           aKeys;         /* List of Keys (Hashed By)                                */
   HashTableObject*     aObjects;      /* List of Pointers to the stored objects                  */
   int                  iCapacity;     /* The Capacity of the Key and Object lists                */
   int                  iCount;        /* The count of the objects (and keys) that fill the list  */
   HashTableEntry*      aHash;         /* Hash Entries                                            */
   int                  iHashSize;     /* Size of Hash Entries                                    */
   double               dFull;         /* Fill Size                                               */
   int                  iRemoveCount;  /* Removed Count                                           */
   };

/*==============================================================================*/
/* Message                                                                      */
/*------------------------------------------------------------------------------*/
/* Maintains the information sent in a single transmission of co-simulation.    */
/* the valid-time and values are stored and can be queries                      */
/*                                                                              */
/* This is a node in a linked list of received messages                         */
/*==============================================================================*/

/*===================================================================*/
/* Constructor / Destructor                                          */
/*===================================================================*/
static Message * EmtdcCosimulation_Message_Create(int size);
static void EmtdcCosimulation_Message_Delete(Message * _this);

/*-------------------------------------------------------------------*/
/* Structure                                                         */
/*-------------------------------------------------------------------*/
struct  EmtdcCosimulation_Message_S
   {
   double         dValidTime;    /* The time that this message is valid until */
   double *       pData;         /* The data for the message                  */
   Message *      pNextMessage;  /* The next received message                 */
   };

/*==============================================================================*/
/* Buffer                                                                       */
/*------------------------------------------------------------------------------*/
/* Maintains the life of an arbitrary sized data buffer                         */
/*==============================================================================*/

/*===================================================================*/
/* Constructor / Destructor                                          */
/*===================================================================*/
static Buffer* EmtdcCosimulation_Buffer_Create();
static void  EmtdcCosimulation_Buffer_Delete(Buffer *_this);

/*-------------------------------------------------------------------*/
/* Member Functions                                                  */
/*-------------------------------------------------------------------*/
static void * EmtdcCosimulation_Buffer_GetBuffer(Buffer * _this, int size);

/*-------------------------------------------------------------------*/
/* Structure                                                         */
/*-------------------------------------------------------------------*/
struct EmtdcCosimulation_Buffer_S
   {
   int iSize;
   void * pBuffer;
   void * (*GetBuffer)(Buffer * _this, int size);
   };

/*=============================================================================================================*/
/* Channel                                                                                                     */
/*-------------------------------------------------------------------------------------------------------------*/
/* The manager for a specific channel of information traveling between this                                    */
/* Client and another client, the channel should be globally unique across the                                 */
/* entire system                                                                                               */
/*=============================================================================================================*/

/*=============================================================================================================*/
/* Constructor                                                                                                 */
/*=============================================================================================================*/
static EmtdcCosimulation_Channel * EmtdcCosimulation_Channel_Create(unsigned short client_id, unsigned int channel_id, int recv_size, int send_size)
   {
   EmtdcCosimulation_Channel * _this;

   _this = malloc(sizeof(EmtdcCosimulation_Channel));
   _this->pReserved = EmtdcCosimulation_Channel_Impl_Create(client_id, channel_id, recv_size, send_size);
   _this->GetValue = &EmtdcCosimulation_Channel_GetValue;
   _this->SetValue = &EmtdcCosimulation_Channel_SetValue;
   _this->Send = &EmtdcCosimulation_Channel_Send;
   _this->GetChannelId = &EmtdcCosimulation_Channel_GetChannelId;
   _this->GetSendSize = &EmtdcCosimulation_Channel_GetSendSize;
   _this->GetRecvSize = &EmtdcCosimulation_Channel_GetRecvSize;
   return _this;
   }

/*=============================================================================================================*/
/* Destructor                                                                                                  */
/*=============================================================================================================*/
static void EmtdcCosimulation_Channel_Delete(EmtdcCosimulation_Channel* _this)
   {
   if (_this == NULL)
      return;

   EmtdcCosimulation_Channel_Impl_Delete((ChannelImpl*)_this->pReserved);
   free(_this);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_GetValue()                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
static double EmtdcCosimulation_Channel_GetValue(EmtdcCosimulation_Channel* _this, double time, int index)
   {
   ChannelImpl * impl;

   impl = (ChannelImpl*)_this->pReserved;
   return EmtdcCosimulation_Channel_Impl_GetValue(impl, time, index);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_SetValue()                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
static void EmtdcCosimulation_Channel_SetValue        (EmtdcCosimulation_Channel* _this, double val, int index)
   {
   ChannelImpl * impl;

   impl = (ChannelImpl*)_this->pReserved;
   EmtdcCosimulation_Channel_Impl_SetValue(impl, val, index);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Send()                                                                            */
/*-------------------------------------------------------------------------------------------------------------*/
static void EmtdcCosimulation_Channel_Send(EmtdcCosimulation_Channel* _this, double time)
   {
   ChannelImpl * impl;

   impl = (ChannelImpl*)_this->pReserved;
   EmtdcCosimulation_Channel_Impl_Send(impl, time);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_GetChannelId()                                                                    */
/*-------------------------------------------------------------------------------------------------------------*/
static unsigned int EmtdcCosimulation_Channel_GetChannelId(EmtdcCosimulation_Channel* _this)
   {
   ChannelImpl * impl;

   impl = (ChannelImpl*)_this->pReserved;
   return impl->iChannelId;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_GetSendSize()                                                                     */
/*-------------------------------------------------------------------------------------------------------------*/
static int EmtdcCosimulation_Channel_GetSendSize(EmtdcCosimulation_Channel* _this)
   {
   ChannelImpl * impl;

   impl = (ChannelImpl*)_this->pReserved;
   return impl->iSendSize;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_GetRecvSize()                                                                     */
/*-------------------------------------------------------------------------------------------------------------*/
static int EmtdcCosimulation_Channel_GetRecvSize(EmtdcCosimulation_Channel* _this)
   {
   ChannelImpl * impl = (ChannelImpl*)_this->pReserved;
   return impl->iRecvSize;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_GetNextChannelMessage()                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
static unsigned int EmtdcCosimulation_Channel_Impl_GetNextChannelMessage(unsigned short client_id)
   {
   int size;
   void * buffer;
   int channel_id;
   EmtdcCosimulation_Channel * ch;

   /* Wait for the next message from the client */
   /**/
   size = CommunicationFabric_Peek_Client(client_id, NULL, 0, 0);
   if ( size > sizeof(unsigned int)  )
      {
      /* Extract the message from the client */
      /**/
      buffer = pEmtdcCosimulation_Channel_Impl_Buffer->GetBuffer(pEmtdcCosimulation_Channel_Impl_Buffer, size);
      if ( CommunicationFabric_Recv_Client(client_id, buffer, pEmtdcCosimulation_Channel_Impl_Buffer->iSize, 0) > sizeof(unsigned int) )
         {
         /* Extract the channel ID the message is intended for. */
         /**/
         EmtdcCosimulation_Extract_int32(buffer, &channel_id);

         /* Multiplex the message to the correct channel and parse the message for processing */
         /**/
         ch = (EmtdcCosimulation_Channel*)EmtdcCosimulation_HashTable_Fetch(pEmtdcCosimulation_ChannelManager, channel_id);
         if (ch != NULL)
            EmtdcCosimulation_Channel_Impl_Parse(((ChannelImpl *)ch->pReserved), buffer, size);
         return channel_id;
         }
      }

   /* No Data Received.                                                       */
   /* This should be impossible as both a blocking Peek and Receive are used  */
   /**/
   assert(0);
   return -1;
   }

/*=============================================================================================================*/
/* Constructor                                                                                                 */
/*=============================================================================================================*/
static ChannelImpl * EmtdcCosimulation_Channel_Impl_Create(unsigned short client_id, unsigned int channel_id, int recv_size, int send_size)
   {
   ChannelImpl * _this;

   /* Allocate memory */
   /**/
   _this = (ChannelImpl*)malloc(sizeof(ChannelImpl));

   /* Set the members of the structure */
   /**/
   _this->iClientId = client_id;
   _this->iChannelId = channel_id;
   _this->iRecvSize = recv_size;
   _this->iSendSize = send_size;
   _this->pRecvMessageBuffer = EmtdcCosimulation_Message_Create(recv_size);
   _this->pSendMessage = EmtdcCosimulation_Message_Create(send_size);
   _this->pLastMessage = EmtdcCosimulation_Message_Create(send_size);
   _this->pRecvMessage = NULL;
   _this->iMessageSize = (unsigned short)(sizeof(int) + sizeof(double) + sizeof(double)*send_size);

   /* Increment the counter of the number of structure in existence. */
   /* if this is the first allocation, allocate a shared buffer for  */
   /* all channels to use when sending or receiving                  */
   /**/
   if (iEmtdcCosimulation_Channel_Impl_Master == 0)
      pEmtdcCosimulation_Channel_Impl_Buffer = EmtdcCosimulation_Buffer_Create();
   iEmtdcCosimulation_Channel_Impl_Master++;

   return _this;
   }

/*=============================================================================================================*/
/* Destructor                                                                                                  */
/*=============================================================================================================*/
static void EmtdcCosimulation_Channel_Impl_Delete(ChannelImpl* _this)
   {
   /* Ensure that the parameter is not null */
   /**/
   if (_this == NULL)
      return;

   /* Deallocate the cached messages */
   /**/
   if (_this->pSendMessage != NULL)
      EmtdcCosimulation_Message_Delete(_this->pSendMessage);

   if (_this->pLastMessage != NULL)
      EmtdcCosimulation_Message_Delete(_this->pLastMessage);

   if (_this->pRecvMessage != NULL)
      EmtdcCosimulation_Message_Delete(_this->pRecvMessage);

   if (_this->pRecvMessage != NULL)
      EmtdcCosimulation_Message_Delete(_this->pRecvMessageBuffer);

   /* decrement the counter for the number of structures in existence.   */
   /* If this is the last structure deallocate the shared buffer         */
   /**/
   if (--iEmtdcCosimulation_Channel_Impl_Master == 0)
      {
      EmtdcCosimulation_Buffer_Delete(pEmtdcCosimulation_Channel_Impl_Buffer);
      pEmtdcCosimulation_Channel_Impl_Buffer = NULL;
      }

   /* Deallocate the memory for the structure itself  */
   /**/
   free(_this);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_GetValue()                                                                   */
/*-------------------------------------------------------------------------------------------------------------*/
static double EmtdcCosimulation_Channel_Impl_GetValue(ChannelImpl* _this, double time, int i)
   {
   Message * prev_msg;
   Message * recv_msg;

   if ( i >= _this->iRecvSize )
      return 0.0; /* Bad data */

   while (1)
      {
      /* Find the Value if already received */
      /**/
      prev_msg = NULL;
      recv_msg = _this->pRecvMessage;
      while (recv_msg != NULL && recv_msg->dValidTime < time )
         {
         prev_msg = recv_msg;
         recv_msg = recv_msg->pNextMessage;
         }

      /* Moved consumed messages to the reuse buffer */
      /**/
      if ( prev_msg != NULL )
         {
         prev_msg->pNextMessage = _this->pRecvMessageBuffer;
         _this->pRecvMessageBuffer = _this->pRecvMessage;
         _this->pRecvMessage = recv_msg;
         }

      /* If the value was received then return  */
      /* the expected value                     */
      /**/
      if ( _this->pRecvMessage != NULL )
         return _this->pRecvMessage->pData[i];

      /* Retrieve messages until we get the time we are looking for */
      /**/
      while (EmtdcCosimulation_Channel_Impl_GetNextChannelMessage(_this->iClientId) != _this->iChannelId);
      }

   /* should not have been able to get here; */
   /**/
   return 0.0;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_SetValue()                                                                   */
/*-------------------------------------------------------------------------------------------------------------*/
static void EmtdcCosimulation_Channel_Impl_SetValue(ChannelImpl* _this, double d, int i)
   {
   if ( i < _this->iSendSize )
      _this->pSendMessage->pData[i] = d;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_Send()                                                                       */
/*-------------------------------------------------------------------------------------------------------------*/
static void EmtdcCosimulation_Channel_Impl_Send(ChannelImpl* _this, double time)
   {
   void * buffer;
   char * ptr;
   int i;
   int n;

   /* Get a buffer ready to send */
   /**/
   buffer = pEmtdcCosimulation_Channel_Impl_Buffer->GetBuffer(pEmtdcCosimulation_Channel_Impl_Buffer, _this->iMessageSize);
   ptr = (char*)buffer;

   /* Set the channel id and the valid time as the header value */
   /**/
   ptr = EmtdcCosimulation_Channel_Impl_SetValueBufferI(_this, ptr, _this->iChannelId);
   ptr = EmtdcCosimulation_Channel_Impl_SetValueBufferD(_this, ptr, time);

   /* Set each of the values into the buffer */
   /**/
   n = _this->iSendSize;
   for ( i = 0 ; i < n; i++)
      {
      ptr = EmtdcCosimulation_Channel_Impl_SetValueBufferD(_this, ptr, _this->pSendMessage->pData[i]);
      _this->pLastMessage->pData[i] = _this->pSendMessage->pData[i];
      _this->pSendMessage->pData[i] = 0;
      }

   /* Send the buffer to the specified client */
   /**/
   CommunicationFabric_Send_Client(_this->iClientId, buffer, _this->iMessageSize, 0);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_Parse()                                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
static void EmtdcCosimulation_Channel_Impl_Parse(ChannelImpl* _this, void * _ptr, int size)
   {
   int channel_id;
   int message_size;
   void * ptr;
   int i;
   int n;
   Message * last;

   message_size = sizeof(unsigned int) + sizeof(double) + _this->iRecvSize;
   ptr = _ptr;
   if ( size >= message_size)
      {
      /* Extract the channel Id From the message */
      /**/
      ptr = EmtdcCosimulation_Extract_int32(ptr, &channel_id);

      /* If there is no cached message ready to receive, create a new one */
      /**/
      if ( _this->pRecvMessageBuffer == NULL )
         _this->pRecvMessageBuffer = EmtdcCosimulation_Message_Create(_this->iRecvSize);

      /* Extract the time that these values are valid for */
      /**/
      ptr = EmtdcCosimulation_Extract_double(ptr, &(_this->pRecvMessageBuffer->dValidTime));

      /* Extract each of the values */
      /**/
      n = _this->iRecvSize;
      for ( i = 0; i < n; i++)
         ptr = EmtdcCosimulation_Extract_double(ptr, &(_this->pRecvMessageBuffer->pData[i]));

      if ( _this->pRecvMessage == NULL )
         {
         /* If there is no current message in the receive queue, set this message to the current one */
         /**/
         _this->pRecvMessage = _this->pRecvMessageBuffer;
         _this->pRecvMessageBuffer = _this->pRecvMessageBuffer->pNextMessage;
         _this->pRecvMessage->pNextMessage = NULL;
         }
      else
         {
         /* If there is a message in the receive queue set this message as the last node */
         /**/
         last = _this->pRecvMessage;
         while (last->pNextMessage != NULL)
            last = last->pNextMessage;

         last->pNextMessage = _this->pRecvMessageBuffer;
         _this->pRecvMessageBuffer = _this->pRecvMessageBuffer->pNextMessage;
         last->pNextMessage->pNextMessage = NULL;
         }
      }
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_SetValueBufferI()                                                            */
/*-------------------------------------------------------------------------------------------------------------*/
static char * EmtdcCosimulation_Channel_Impl_SetValueBufferI(ChannelImpl* _this, char* ptr, unsigned int val)
   {
   *((unsigned int*)ptr) = EmtdcCosimulation_Marshal_int32(val);
   return ptr + sizeof(unsigned int);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_SetValueBufferD()                                                            */
/*-------------------------------------------------------------------------------------------------------------*/
static char * EmtdcCosimulation_Channel_Impl_SetValueBufferD(ChannelImpl* _this, char* ptr, double val)
   {
   *((double*)ptr) = EmtdcCosimulation_Marshal_double(val);
   return ptr + sizeof(double);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Channel_Impl_Send_Final()                                                            */
/*-------------------------------------------------------------------------------------------------------------*/
static void  EmtdcCosimulation_Channel_Impl_Send_Final(ChannelImpl* _this)
   {
   void* buffer;
   char* ptr;
   int i;
   int n;

   /* Get a buffer ready to send */
   /**/
   buffer = pEmtdcCosimulation_Channel_Impl_Buffer->GetBuffer(pEmtdcCosimulation_Channel_Impl_Buffer, _this->iMessageSize);
   ptr = (char*)buffer;

   /* Set the channel id and the valid time as the header value                        */
   /* As this is the final send the time will be set to the maximum double value       */
   /* this indicates an unlimited amount of time. This value is valid from the last    */
   /* message sent until the simulation is complete.                                   */
   /**/
   ptr = EmtdcCosimulation_Channel_Impl_SetValueBufferI(_this, ptr, _this->iChannelId);
   ptr = EmtdcCosimulation_Channel_Impl_SetValueBufferD(_this, ptr, DBL_MAX);

   /* Set each of the values into the buffer */
   /**/
   n = _this->iSendSize;
   for (i = 0; i < n; i++)
      ptr = EmtdcCosimulation_Channel_Impl_SetValueBufferD(_this, ptr, _this->pLastMessage->pData[i]);

   /* Send the buffer to the specified client */
   /**/
   CommunicationFabric_Send_Client(_this->iClientId, buffer, _this->iMessageSize, 0);
   }

/*-------------------------------------------------------------------*/
/* Structure                                                         */
/*-------------------------------------------------------------------*/
struct EmtdcCosimulation_InitData_S
   {
   const char* sFabricLocation;
   const char* sHostName;
   int iPort;
   int iClientId;
   double dTime;
   double dStep;
   };

/*=============================================================================================================*/
/* EmtdcCosimulation_InitializeCosimulationImpl                                                                */
/*-------------------------------------------------------------------------------------------------------------*/
/* IMplementation of initialization this should only be called once                                            */
/*=============================================================================================================*/
static void EmtdcCosimulation_InitializeCosimulationImpl(InitData* data)
   {
   char s_port[10];
   char s_id[10];
   char* exe_path;
   char* cmp_name;
   const int iargs = 9;
   char* args[9];
   int peek_size;
   void* _buffer;
   void* send_buffer;
   int com_size;
   int header;
   int channel_count;
   int message_size;
   int i;
   int n;
   int client_id2;
   int channel_id;
   int send_size;
   int recv_size;
   int pid;
   unsigned long cmp_name_size;
   EmtdcCosimulation_Channel* new_channel;
   Buffer* buffer;
   HMODULE hModule;

   /* Load the communication fabric */
   /**/
   if (CommunicationFabric_Load(data->sFabricLocation) == 0)
      return;

   /* If this has already been initialized do not initialize again */
   /**/
   if (pEmtdcCosimulation_ChannelManager != NULL)
      return;

   /* Copy the parameters to be used during the finalization process */
   /**/
   iEmtdcCosimulation_ClientId = data->iClientId;
   iEmtdcCosimulation_Port = data->iPort;
   strcpy_s(sEmtdcCosimulation_HostName, 256, data->sHostName);
   dEmtdcCosimulation_Time = data->dTime;
   dEmtdcCosimulation_Step = data->dStep;

   /* Convert the integers to strings to pass in as arguments */
   /**/
   _itoa_s(iEmtdcCosimulation_Port, s_port, 10, 10);
   _itoa_s(iEmtdcCosimulation_ClientId, s_id, 10, 10);

   /* Get the executable path */
   /**/
   exe_path = malloc(sizeof(char) * MAX_PATH);
   hModule = GetModuleHandle(NULL);
   GetModuleFileNameA(hModule, exe_path, MAX_PATH);

   /* Construct the arguments */
   /**/
   args[0] = exe_path;
   args[1] = "/API";
   args[2] = "TCP";
   args[3] = "/HOST";
   args[4] = sEmtdcCosimulation_HostName;
   args[5] = "/PORT";
   args[6] = s_port;
   args[7] = "/ID";
   args[8] = s_id;

   /* Initialize the Communication Fabric                               */
   /* (When this process returns all connection will be established)    */
   /**/
   CommunicationFabric_Initialize(iargs, args);

   /* Construct a new Channel manager to process the channels */
   /**/
   pEmtdcCosimulation_ChannelManager = EmtdcCosimulation_HashTable_Create(0.75);

   /* Check Message Size of the incoming Channel Map from the master (PSCAD) */
   /**/
   peek_size = CommunicationFabric_Peek_Server(0, NULL, 0, 0);

   /* Allocate a buffer large enough for the Map */
   /**/
   buffer = EmtdcCosimulation_Buffer_Create();
   _buffer = buffer->GetBuffer(buffer, peek_size);

   /* Receive the Map from the master (PSCAD) */
   /**/
   com_size = CommunicationFabric_Recv_Server(0, _buffer, peek_size, 0);

   /* Ensure the message is large enough to contain the meta-data on the map itself */
   /**/
   assert(com_size >= (sizeof(int) + sizeof(int)));
   if (com_size >= (sizeof(int) + sizeof(int)))
      {
      /* Extract the header to ensure the communication is transmitting correctly  */
      /* and extract the count of channel contains in the message                  */
      /**/
      _buffer = EmtdcCosimulation_Extract_int32(_buffer, &header);
      _buffer = EmtdcCosimulation_Extract_int32(_buffer, &channel_count);

      message_size = sizeof(int) + sizeof(int) + (sizeof(int) * 4 * channel_count);

      /* Ensure the header is valid and the message sent is large enough to contain the entire  */
      /* map                                                                                    */
      /**/
      assert(header == 0xCAFEF00D);
      assert(com_size >= message_size);
      if (header == 0xCAFEF00D && com_size >= message_size)
         {
         /* Construct a new channel for each channel passed in through this           */
         /* message                                                                   */
         /**/
         n = channel_count;
         for (i = 0; i < n; i++)
            {
            /* Extract the information about the channel */
            /**/
            _buffer = EmtdcCosimulation_Extract_int32(_buffer, &client_id2);
            _buffer = EmtdcCosimulation_Extract_int32(_buffer, &channel_id);
            _buffer = EmtdcCosimulation_Extract_int32(_buffer, &send_size);
            _buffer = EmtdcCosimulation_Extract_int32(_buffer, &recv_size);

            /* Construct a new Channel */
            /**/
            new_channel = EmtdcCosimulation_Channel_Create(client_id2, channel_id, recv_size / sizeof(double), send_size / sizeof(double));

            /* Add the Channel to the Hash-Table Manager of the Channels */
            /**/
            EmtdcCosimulation_HashTable_Append(pEmtdcCosimulation_ChannelManager, new_channel, channel_id);
            }
         }
      }


   /* Send identification information back to the master */
   /**/
   cmp_name_size = MAX_COMPUTERNAME_LENGTH + 1;
   cmp_name = malloc(sizeof(char) * cmp_name_size);
   GetComputerNameA(cmp_name, &cmp_name_size);
   pid = GetCurrentProcessId();
   send_size = (int)(sizeof(int) + sizeof(char) * strlen(cmp_name) + 1);

   send_buffer = buffer->GetBuffer(buffer, send_size);
   _buffer = EmtdcCosimulation_Insert_int32(send_buffer, pid);
   _buffer = EmtdcCosimulation_Insert_string(_buffer, cmp_name);

   CommunicationFabric_Send_Server(0, send_buffer, (unsigned short)send_size, 0);

   /* Ensure Buffer is cleaned up */
   /**/
   EmtdcCosimulation_Buffer_Delete(buffer);
   free(exe_path);
   }

/*=============================================================================================================*/
/* InitializeCosimulation                                                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
/* Call this function to start the Co-Simulation Process. Only call this                                       */
/* function once per process. This version of the function accepts the                                         */
/* host-name and the port directly                                                                             */
/*=============================================================================================================*/
void   EmtdcCosimulation_InitializeCosimulation(const char* fabric_location, const char* hostname, int port, int client_id)
   {
   InitData data;
   data.sFabricLocation = fabric_location;
   data.sHostName = hostname;
   data.iPort = port;
   data.iClientId = client_id;
   data.dTime = 0;
   data.dStep = 0;
   EmtdcCosimulation_InitializeCosimulationImpl(&data);
   }

/*=============================================================================================================*/
/* InitializeCosimulation                                                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
/* Call this function to start the Co-Simulation Process. Only call this                                       */
/* function once per process. This version of the function accepts the accepts                                 */
/* the host and port as a configuration file.                                                                  */
/*=============================================================================================================*/
void  EmtdcCosimulation_InitializeCosimulationCfg(const char * cfg_path)
   {
   const char * TAG_CLIENT;
   const char * TAG_VERSION;
   const char * TAG_ADDRESS;
   const char * TAG_PORT;
   const char * TAG_COMFAB_x86;
   const char * TAG_COMFAB_x64;
   const char * TAG_TIME;
   const char * TAG_STEP;

   int MAX_LINE_LENGTH;
   int MAX_IPADDRESS_LENGTH;
   int TAG_SIZE_CLIENT;
   int TAG_SIZE_VERSION;
   int TAG_SIZE_ADDRESS;
   int TAG_SIZE_PORT;
   int TAG_SIZE_COMFAB_x86;
   int TAG_SIZE_COMFAB_x64;
   int TAG_SIZE_TIME;
   int TAG_SIZE_STEP;

   FILE *   file;
   char*    _line;
   int      version;
   int      client_id;
   char *   ipaddress;
   char *   comfab_x86;
   char *   comfab_x64;
   int      port;
   double   time;
   double   step;

   InitData data;
   memset(&data, 0, sizeof(InitData));

   /* Initialize Memory required to read the file */
   /**/
   MAX_LINE_LENGTH = 1024;
   MAX_IPADDRESS_LENGTH = 256;

   file = NULL;
   _line = NULL;
   version = 0;
   ipaddress = NULL;
   port = 0;
   client_id = -1;
   time = 0.0;
   step = 0.0;

   TAG_CLIENT = "Client:";
   TAG_VERSION = "Version:";
   TAG_ADDRESS = "Address:";
   TAG_PORT    = "Port:";
   TAG_COMFAB_x86 = "ComFabx86:";
   TAG_COMFAB_x64 = "ComFabx64:";
   TAG_TIME = "Time:";
   TAG_STEP = "Step:";

   TAG_SIZE_CLIENT = (int)strlen(TAG_CLIENT);
   TAG_SIZE_VERSION = (int)strlen(TAG_VERSION);
   TAG_SIZE_ADDRESS = (int)strlen(TAG_ADDRESS);
   TAG_SIZE_PORT = (int)strlen(TAG_PORT);
   TAG_SIZE_COMFAB_x86 = (int)strlen(TAG_COMFAB_x86);
   TAG_SIZE_COMFAB_x64 = (int)strlen(TAG_COMFAB_x64);
   TAG_SIZE_TIME = (int)strlen(TAG_TIME);
   TAG_SIZE_STEP = (int)strlen(TAG_STEP);

   _line = (char*)malloc(sizeof(char) * MAX_LINE_LENGTH);
   ipaddress = (char*)malloc(sizeof(char) * MAX_IPADDRESS_LENGTH);
   comfab_x86 = (char*)malloc(sizeof(char) * MAX_PATH);
   comfab_x64 = (char*)malloc(sizeof(char) * MAX_PATH);

   memset(ipaddress, 0, sizeof(char) * MAX_IPADDRESS_LENGTH);
   memset(comfab_x86, 0, sizeof(char) * MAX_PATH);
   memset(comfab_x64, 0, sizeof(char) * MAX_PATH);

   /* The Configuration file should be next to the running *.exe so, the path is modified to search   */
   /* for the expected file                                                                           */
   /**/
   if (fopen_s(&file, cfg_path, "r") != 0)
      return;

   /* Read and parse the enire file */
   /**/
   while (!feof(file))
      {
      /* Read the line */
      /**/
      if (fgets(_line, MAX_LINE_LENGTH, file) != NULL)
         {
         /* If the line begins with the VERSION specified then switch versions for the information being read. */
         /* */
         if (strnicmp(TAG_VERSION, _line, TAG_SIZE_VERSION) == 0)
            {
            /* Read the version, if the version number is invalid, reset the version to 0, as nothing to be parsed. */
            /**/
            if (sscanf_s(_line + TAG_SIZE_VERSION, "%d", &version) != 1)
               version = 0;
            }

         else if (version == 1)
            {
            if (strnicmp(TAG_CLIENT, _line, TAG_SIZE_CLIENT) == 0)
               {
               if (sscanf_s(_line + TAG_SIZE_CLIENT, "%d", &client_id) != 1)
                  client_id = -1;
               }
            else if (strnicmp(TAG_ADDRESS, _line, TAG_SIZE_ADDRESS) == 0)
               {
               if (sscanf_s(_line + TAG_SIZE_ADDRESS, "%256s", ipaddress, MAX_IPADDRESS_LENGTH) != 1)
                  strcpy_s(ipaddress, MAX_IPADDRESS_LENGTH, "");
               }
            else if (strnicmp(TAG_PORT, _line, TAG_SIZE_PORT) == 0)
               {
               if (sscanf_s(_line + TAG_SIZE_PORT, "%d", &port) != 1)
                  port = -1;
               }
            else if (strnicmp(TAG_COMFAB_x86, _line, TAG_SIZE_COMFAB_x86) == 0)
               {
               strcpy_s(comfab_x86, MAX_PATH, _line + TAG_SIZE_COMFAB_x86);
               }
            else if (strnicmp(TAG_COMFAB_x64, _line, TAG_SIZE_COMFAB_x64) == 0)
               {
               strcpy_s(comfab_x64, MAX_PATH, _line + TAG_SIZE_COMFAB_x64);
               }
            else if (strnicmp(TAG_TIME, _line, TAG_SIZE_TIME) == 0)
               {
               if (sscanf_s(_line + TAG_SIZE_TIME, "%lf", &time) != 1)
                  time = 0.0;
               }
            else if (strnicmp(TAG_STEP, _line, TAG_SIZE_STEP) == 0)
               {
               if (sscanf_s(_line + TAG_SIZE_STEP, "%lf", &step) != 1)
                  step = 0.0;
               }
            }
         }
      }

   /* Close and free required memory, and resources */
   /**/
   fclose(file);
   free(_line);
   _line = NULL;

   /* Perform normal initialization */
   /**/
   if (port > 0 && client_id > 0 && ipaddress[0] != '\0' && comfab_x86[0] != '\0' && comfab_x64[0] != '\0')
      {
      if (sizeof(char*) == 4)
         data.sFabricLocation = EmtdcCosimulation_string_trim(comfab_x86);
      else if (sizeof(char*) == 8)
         data.sFabricLocation = EmtdcCosimulation_string_trim(comfab_x64);
      data.sHostName = ipaddress;
      data.iClientId = client_id;
      data.iPort = port;
      data.dTime = time;
      data.dStep = step;
      EmtdcCosimulation_InitializeCosimulationImpl(&data);
      }

   free(ipaddress);
   free(comfab_x86);
   free(comfab_x64);
   ipaddress = NULL;
   }

/*=============================================================================================================*/
/* FindChannel()                                                                                               */
/*-------------------------------------------------------------------------------------------------------------*/
/* Get the channel with the channel_id specified (if it exists)                                                */
/*=============================================================================================================*/
EmtdcCosimulation_Channel *   EmtdcCosimulation_FindChannel(unsigned int channel_id)
   {
   if (pEmtdcCosimulation_ChannelManager != NULL)
      return (EmtdcCosimulation_Channel*)EmtdcCosimulation_HashTable_Fetch(pEmtdcCosimulation_ChannelManager, channel_id);
   return NULL;
   }

/*=============================================================================================================*/
/* FinalizeCosimulation                                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
/* Call this function to end the Co-Simulation process                                                         */
/*=============================================================================================================*/
void  EmtdcCosimulation_FinalizeCosimulation()
   {
   char s_port[10];
   char s_id[10];
   const int iargs = 9;
   char * args[9];
   char*  exe_path;
   HMODULE hModule;
   int message;
   int i, n;
   EmtdcCosimulation_Channel* channel;
   ChannelImpl* channel_imp;

   /* If the Co-Simulation has not been initialized then */
   /* it cannot be finalized                             */
   /**/
   if (pEmtdcCosimulation_ChannelManager == NULL)
      return;

   /* Resend the last message with unlimited expiration date. This will ensure */
   /* that the simulation will not stall if the timings are slightly off       */
   /**/
   n = EmtdcCosimulation_HashTable_GetCount(pEmtdcCosimulation_ChannelManager);
   for (i = 0; i < n; i++)
      {
      channel = EmtdcCosimulation_HashTable_Get(pEmtdcCosimulation_ChannelManager, i);
      if (channel != NULL && EmtdcCosimulation_Channel_GetSendSize(channel) > 0)
         {
         channel_imp = (ChannelImpl*)channel->pReserved;
         if (channel_imp != NULL)
            EmtdcCosimulation_Channel_Impl_Send_Final(channel_imp);
         }
      }

   /* Receive all data until the end of the simulation to ensure the buffer is emptied */
   /**/
   if (dEmtdcCosimulation_Time > 0)
      {
      n = EmtdcCosimulation_HashTable_GetCount(pEmtdcCosimulation_ChannelManager);
      for (i = 0; i < n; i++)
         {
         channel = EmtdcCosimulation_HashTable_Get(pEmtdcCosimulation_ChannelManager, i);
         if (channel != NULL && EmtdcCosimulation_Channel_GetRecvSize(channel) > 0)
            EmtdcCosimulation_Channel_GetValue(channel, dEmtdcCosimulation_Time, 0);
         }
      }

   /* Send a complete message */
   /**/
   message = 0xFFFF;
   CommunicationFabric_Send_Server(0, &message, sizeof(int), 0);

   /* Reconstruct the argument list */
   /**/
   _itoa_s(iEmtdcCosimulation_Port, s_port, 10, 10);
   _itoa_s(iEmtdcCosimulation_ClientId, s_id, 10, 10);

   exe_path = malloc(sizeof(char) * MAX_PATH);
   hModule = GetModuleHandle(NULL);
   GetModuleFileNameA(hModule, exe_path, MAX_PATH);

   /* Construct the arguments */
   /**/
   args[0] = exe_path;
   args[1] = "/API";
   args[2] = "TCP";
   args[3] = "/HOST";
   args[4] = sEmtdcCosimulation_HostName;
   args[5] = "/PORT";
   args[6] = s_port;
   args[7] = "/ID";
   args[8] = s_id;

   /* Finalize the communication fabric, this will disconnect and shut down all communication */
   /**/
   CommunicationFabric_Finalize(iargs, args);

   /* Delete and reset the channel manager */
   /**/
   n = EmtdcCosimulation_HashTable_GetCount(pEmtdcCosimulation_ChannelManager);
   for (i = 0; i < n; i++)
      EmtdcCosimulation_Channel_Delete((EmtdcCosimulation_Channel*)EmtdcCosimulation_HashTable_Get(pEmtdcCosimulation_ChannelManager, i));

   EmtdcCosimulation_HashTable_Delete(pEmtdcCosimulation_ChannelManager);
   pEmtdcCosimulation_ChannelManager = NULL;

   /* Clean up and remove the communication fabric */
   CommunicationFabric_Unload();

   free(exe_path);
   }

/*=============================================================================================================*/
/* CommunicationFabric                                                                                         */
/*-------------------------------------------------------------------------------------------------------------*/
/* This namespace contains the calls into the Communication Fabric DLL.                                        */
/*-------------------------------------------------------------------------------------------------------------*/

/*-------------------------------------------------------------------------------------------------------------*/
/* Load()                                                                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Load(const char * location)
   {
   hComFabLibrary = LoadLibraryA(location);
   if ( hComFabLibrary != NULL )
      {
      _CommunicationFabric_Initialize  = (CommunicationFabric_Init_Func)GetProcAddress(hComFabLibrary,"Communication_Initialize");
	   _CommunicationFabric_Finalize    = (CommunicationFabric_Init_Func)GetProcAddress(hComFabLibrary,"Communication_Finalize");
	   _CommunicationFabric_Send_Client = (CommunicationFabric_Com_Func)GetProcAddress(hComFabLibrary,"Communication_send_client");
	   _CommunicationFabric_Recv_Client = (CommunicationFabric_Com_Func)GetProcAddress(hComFabLibrary,"Communication_recv_client");
	   _CommunicationFabric_Peek_Client = (CommunicationFabric_Com_Func)GetProcAddress(hComFabLibrary,"Communication_peek_client");
	   _CommunicationFabric_Send_Server = (CommunicationFabric_Com_Func)GetProcAddress(hComFabLibrary,"Communication_send_server");
	   _CommunicationFabric_Recv_Server = (CommunicationFabric_Com_Func)GetProcAddress(hComFabLibrary,"Communication_recv_server");
	   _CommunicationFabric_Peek_Server = (CommunicationFabric_Com_Func)GetProcAddress(hComFabLibrary,"Communication_peek_server");
      if (  _CommunicationFabric_Initialize   != NULL && _CommunicationFabric_Finalize     != NULL
         && _CommunicationFabric_Send_Client  != NULL && _CommunicationFabric_Recv_Client  != NULL   && _CommunicationFabric_Peek_Client  != NULL
         && _CommunicationFabric_Send_Server  != NULL && _CommunicationFabric_Recv_Server  != NULL   && _CommunicationFabric_Peek_Server  != NULL)
         {
         return 1;
         }
      }
   return 0;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_Unload()                                                                                */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Unload()
   {
   if (hComFabLibrary != NULL)
      {
      /* Reset the Function pointers to NULL */
      /**/
      _CommunicationFabric_Initialize   = NULL;
      _CommunicationFabric_Finalize     = NULL;
      _CommunicationFabric_Send_Client  = NULL;
      _CommunicationFabric_Recv_Client  = NULL;
      _CommunicationFabric_Peek_Client  = NULL;
      _CommunicationFabric_Send_Server  = NULL;
      _CommunicationFabric_Recv_Server  = NULL;
      _CommunicationFabric_Peek_Server  = NULL;

      /* Free the library */
      /**/
      FreeLibrary(hComFabLibrary);

      /* Reset the Module pointer to NULL */
      /**/
      hComFabLibrary = NULL;

      return 1;
      }

   return 0;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_Initialize()                                                                            */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Initialize(int argc, char * args[])
   {
   if ( _CommunicationFabric_Initialize != NULL )
      return _CommunicationFabric_Initialize(argc, args);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_Finalize()                                                                              */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Finalize(int argc, char * args[])
   {
   if ( _CommunicationFabric_Finalize != NULL )
      return _CommunicationFabric_Finalize(argc, args);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_send_client()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Send_Client(unsigned short to, void * buffer, unsigned short size, unsigned short flag)
   {
   if ( _CommunicationFabric_Send_Client != NULL )
      return _CommunicationFabric_Send_Client(to, buffer, size, flag);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_recv_client()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Recv_Client(unsigned short to, void * buffer, unsigned short size, unsigned short flag)
   {
   if ( _CommunicationFabric_Recv_Client != NULL )
      return _CommunicationFabric_Recv_Client(to, buffer, size, flag);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_peek_client()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Peek_Client(unsigned short to, void * buffer, unsigned short size, unsigned short flag)
   {
   if ( _CommunicationFabric_Peek_Client != NULL )
      return _CommunicationFabric_Peek_Client(to, buffer, size, flag);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_send_server()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Send_Server(unsigned short to, void * buffer, unsigned short size, unsigned short flag)
   {
   if ( _CommunicationFabric_Send_Server != NULL )
      return _CommunicationFabric_Send_Server(to, buffer, size, flag);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_recv_server()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Recv_Server(unsigned short to, void * buffer, unsigned short size, unsigned short flag)
   {
   if ( _CommunicationFabric_Recv_Server != NULL )
      return _CommunicationFabric_Recv_Server(to, buffer, size, flag);
   return -10; /* This should not happen */
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* CommunicationFabric_peek_server()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static int CommunicationFabric_Peek_Server(unsigned short to, void * buffer, unsigned short size, unsigned short flag)
   {
   if ( _CommunicationFabric_Peek_Server != NULL )
      return _CommunicationFabric_Peek_Server(to, buffer, size, flag);
   return -10; /* This should not happen */
   }

/*=============================================================================================================*/
/* HashTable                                                                                                   */
/*-------------------------------------------------------------------------------------------------------------*/
/* This is a fast hash-table used to quickly retrieve objects by a hash                                        */
/* identifier                                                                                                  */
/*=============================================================================================================*/

/*=============================================================================================================*/
/* Constructor                                                                                                 */
/*=============================================================================================================*/
static HashTable * EmtdcCosimulation_HashTable_Create(double fill_cap)
   {

   HashTable * _this;

   /* Allocate memory */
   /**/
   _this = (HashTable*)malloc(sizeof(HashTable));
   _this->dFull = fill_cap;
   _this->aHash = (HashTableEntry*)malloc(sizeof(HashTableEntry)*iEmtdcCosimulation_HashTable_StartSize);
   _this->iHashSize = iEmtdcCosimulation_HashTable_StartSize;
   _this->iRemoveCount = 0;
   _this->aKeys = (int*)malloc(sizeof(int)*iEmtdcCosimulation_HashTable_StartCapacity);
   _this->aObjects = (HashTableObject*)malloc(sizeof(HashTableObject)*iEmtdcCosimulation_HashTable_StartCapacity);
   _this->iCapacity = iEmtdcCosimulation_HashTable_StartCapacity;
   _this->iCount = 0;

   /* Initialize Memory */
   /**/
   memset(_this->aHash     , 0, _this->iHashSize   *  sizeof(HashTableEntry));
   memset(_this->aKeys     , 0, _this->iCapacity   *  sizeof(int));
   memset(_this->aObjects  , 0, _this->iCapacity   *  sizeof(HashTableObject));

   return _this;
   }

/*=============================================================================================================*/
/* Destructor                                                                                                  */
/*=============================================================================================================*/
static void EmtdcCosimulation_HashTable_Delete(HashTable * _this)
   {
   /* Ensure the structure exists */
   /**/
   if (_this == NULL)
      return;

   /* Deallocate the internal lists and arrays */
   /**/
   free(_this->aHash);
   free(_this->aKeys);
   free(_this->aObjects);

   /* Deallocate the structure */
   /**/
   free(_this);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_Fetch()                                                                         */
/*-------------------------------------------------------------------------------------------------------------*/
static void*  EmtdcCosimulation_HashTable_Fetch(HashTable * _this, int key)
   {
   int val;

   if (0 < key)
      {
      val = EmtdcCosimulation_HashTable_Hash(_this, key, 0, NULL, 0);
      if (val >= 0 && _this->aHash[val].iKey == key )
         return _this->aObjects[_this->aHash[val].iIndex];
      }
   return NULL;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_Append()                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
static int    EmtdcCosimulation_HashTable_Append(HashTable * _this, void* object, int key)
   {
   int val;

   if (object != NULL && 0 < key)
      {
      EmtdcCosimulation_HashTable_EnsureCapacity(_this, _this->iCount + 1);

      /* By design the object map must have a unique key   */
      /* for each object. Ensure that the key is available */
      /* before adding it to the map.                      */
      /**/
      val = EmtdcCosimulation_HashTable_Hash(_this, key, 1, NULL, 0);
      if (val >= 0 && _this->aHash[val].iKey == 0 || _this->aHash[val].iKey == -1)
         {
         _this->aKeys[_this->iCount] = key;
         _this->aObjects[_this->iCount] = object;
         _this->aHash[val].iIndex = _this->iCount;
         _this->aHash[val].iKey = key;
         _this->iCount++;
         return 1;
         }
      }
   return 0;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_Remove()                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
static int    EmtdcCosimulation_HashTable_Remove(HashTable * _this, int key)
   {
   int val;
   int empty_ratio;
   int min_remove;

   val = EmtdcCosimulation_HashTable_Hash(_this, key, 0, NULL, 0);
   if (val >= 0 && _this->aHash[val].iKey == key )
      {
      int index = _this->aHash[val].iIndex;

      _this->aObjects[index]   = NULL;
      _this->aKeys[index]      = 0;
      _this->aHash[val].iIndex = -1;
      _this->aHash[val].iKey = -1;

      _this->iRemoveCount++;

      empty_ratio = _this->iCount/iEmtdcCosimulation_HashTable_EmptyDivisor;
      min_remove = (empty_ratio > iEmtdcCosimulation_HashTable_EmptyMin) ? empty_ratio : iEmtdcCosimulation_HashTable_EmptyMin;
      if ( _this->iRemoveCount >  min_remove)
         EmtdcCosimulation_HashTable_Rebuild(_this, -1);
      return 1;
      }
   return 0;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_GetCount()                                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
static int    EmtdcCosimulation_HashTable_GetCount(HashTable * _this)
   {
   return _this->iCount;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_GetKey()                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
static int    EmtdcCosimulation_HashTable_GetKey(HashTable * _this, int index)
   {
   if (0 <= index && index < _this->iCount)
      return _this->aKeys[index];
   return -1;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_Get()                                                                           */
/*-------------------------------------------------------------------------------------------------------------*/
static void*  EmtdcCosimulation_HashTable_Get(HashTable * _this, int index)
   {
   if ( 0 <= index && index < _this->iCount )
      return _this->aObjects[index];
   return NULL;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_EnsureCapacity()                                                                */
/*-------------------------------------------------------------------------------------------------------------*/
static void   EmtdcCosimulation_HashTable_EnsureCapacity(HashTable * _this, int size)
   {
   int new_capacity;

   if (_this->iCapacity <= size)
      {
      new_capacity = _this->iCapacity * 2;
      while (new_capacity <= size)
         new_capacity *= 2;

      EmtdcCosimulation_HashTable_Rebuild(_this, new_capacity);
      }
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_Hash()                                                                          */
/*-------------------------------------------------------------------------------------------------------------*/
static int    EmtdcCosimulation_HashTable_Hash(HashTable * _this, int key, int is_new, HashTableEntry* entries, int size)
   {
   unsigned int count;
   unsigned int val;

   /* Invalid key */
   /**/
   assert(key > 0);
   if ( key <= 0 )
      return -1;

   /* Set default values */
   /**/
   if ( entries == NULL )
      {
      entries = _this->aHash;
      size = _this->iHashSize;
      }

   count = 1;

   /* Truncate key to 32 bit unsigned value */
   /**/
   val = (unsigned int)(key + count++);

   /* Apply Magic */
   /**/
   val = ((val >> 16) ^ val) * 0x45d9f3b;
   val = ((val >> 16) ^ val) * 0x45d9f3b;
   val = ((val >> 16) ^ val);
   val = val % size;

   while ( entries[val].iKey != 0 && entries[val].iKey != key && !( is_new == 1 && entries[val].iKey == -1))
      {
      /* apply more magic */
      /**/
      val = (unsigned int)(key + count++);
      val = ((val >> 16) ^ val) * 0x45d9f3b;
      val = ((val >> 16) ^ val) * 0x45d9f3b;
      val = ((val >> 16) ^ val);
      val = val % size;
      }

   return val;
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_HashTable_Rebuild()                                                                       */
/*-------------------------------------------------------------------------------------------------------------*/
static void   EmtdcCosimulation_HashTable_Rebuild(HashTable * _this, int capacity)
   {
   int new_hashsize;
   int * new_keys;
   HashTableObject * new_objects;
   HashTableEntry* new_entries;
   int index;
   int i;
   int n;
   int key;
   int val;
   void * o;

   if ( capacity < 0 )
      capacity = _this->iCapacity;

   new_hashsize = (int)(capacity * (1.0/_this->dFull));

   /* Allocate new lists and hash entries */
   /**/
   new_keys       = (int*)malloc(capacity*sizeof(int));
   new_objects    = malloc(capacity*sizeof(HashTableObject));
   new_entries    = malloc(new_hashsize*sizeof(HashTableEntry));

   /* Initialize new lists and hash entries */
   /**/
   memset(new_keys,0,capacity*sizeof(int));
   memset(new_objects,0,capacity*sizeof(HashTableObject));
   memset(new_entries,0,new_hashsize*sizeof(HashTableEntry));

   /* Copy existing values into new structures */
   /**/
   index = 0;
   n = _this->iCount;
   for ( i = 0; i < n; i++)
      {
      key = _this->aKeys[i];
      o = _this->aObjects[i];
      if ( key > 0 && o != NULL )
         {
         val = EmtdcCosimulation_HashTable_Hash(_this, key, 1, new_entries, new_hashsize);
         if ( val >= 0 )
            {
            new_keys[index] = key;
            new_objects[index] = o;
            new_entries[val].iIndex = index;
            new_entries[val].iKey = key;
            index++;
            }
         else
            return; /* Hashing Error */
         }
      }

   /* Deallocate the old structures */
   /**/
   free(_this->aHash);
   free(_this->aKeys);
   free(_this->aObjects);

   /* Update the existing information */
   /**/
   _this->iCapacity = capacity;
   _this->iHashSize = new_hashsize;

   _this->aHash = new_entries;
   _this->aKeys = new_keys;
   _this->aObjects = new_objects;
   }

/*=============================================================================================================*/
/* Message                                                                                                     */
/*-------------------------------------------------------------------------------------------------------------*/
/* This is a fast hash-table used to quickly retrieve objects by a hash                                        */
/* identifier                                                                                                  */
/*                                                                                                             */
/* This is a node in a linked list of received messages                                                        */
/*=============================================================================================================*/

/*=============================================================================================================*/
/* Constructor                                                                                                 */
/*=============================================================================================================*/
static Message * EmtdcCosimulation_Message_Create(int size)
   {
   Message * _this;

   /* Allocate the structure */
   /**/
   _this = malloc(sizeof(Message));

   /* Set the local members */
   /**/
   _this->dValidTime = 0;
   _this->pData = malloc(sizeof(double)*size);
   _this->pNextMessage = NULL;

   /* Initialize the data to 0s */
   /**/
   memset(_this->pData, 0, sizeof(double)*size);

   return _this;
   }

/*=============================================================================================================*/
/* Destructor                                                                                                  */
/*=============================================================================================================*/
static void EmtdcCosimulation_Message_Delete(Message * _this)
   {
   /* Ensure the structure exists */
   /**/
   if (_this == NULL)
      return;

   /* Delete the next node in the linked list */
   /**/
   if (_this->pNextMessage != NULL)
      EmtdcCosimulation_Message_Delete(_this->pNextMessage);

   /* Deallocate the stored data memory buffer */
   /**/
   free(_this->pData);

   /* Deallocate the structure */
   /**/
   free(_this);
   }

/*=============================================================================================================*/
/* Buffer                                                                                                      */
/*-------------------------------------------------------------------------------------------------------------*/
/* Maintains the life of an arbitrary sized data buffer                                                        */
/*=============================================================================================================*/

/*=============================================================================================================*/
/* Constructor                                                                                                 */
/*=============================================================================================================*/
static Buffer* EmtdcCosimulation_Buffer_Create()
   {
   Buffer * _this;
   _this = malloc(sizeof(Buffer));
   _this->pBuffer = malloc(32);
   _this->iSize = 32;

   _this->GetBuffer = &EmtdcCosimulation_Buffer_GetBuffer;

   return _this;
   }

/*=============================================================================================================*/
/* Destructor                                                                                                  */
/*=============================================================================================================*/
static void  EmtdcCosimulation_Buffer_Delete(Buffer * _this)
   {
   /* Ensure the structure exists */
   /**/
   if (_this == NULL)
      return;

   /* Deallocate the memory buffer */
   /**/
   free(_this->pBuffer);

   /* Deallocate the structure */
   /**/
   free(_this);
   }

/*-------------------------------------------------------------------------------------------------------------*/
/* EmtdcCosimulation_Buffer_GetBuffer()                                                                        */
/*-------------------------------------------------------------------------------------------------------------*/
static void * EmtdcCosimulation_Buffer_GetBuffer(Buffer * _this, int size)
   {
   /* If the currently allocate buffer is too small reallocate the buffer  */
   /* to be large enough to store the complete data                        */
   /**/
   if ( _this->iSize < size )
      {
      _this->pBuffer = realloc(_this->pBuffer, size);
      _this->iSize = size;
      }

   /* Return the internal memory buffer */
   /**/
   return _this->pBuffer;
   }
