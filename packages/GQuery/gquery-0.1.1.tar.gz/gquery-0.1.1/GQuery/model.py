import os# This guide can only be run with the torch backend.
os.environ["KERAS_BACKEND"] = "torch"
from keras.layers import  LayerNormalization, Dense,Activation,BatchNormalization,Embedding,Reshape,Concatenate,Dropout
from keras import Model as tfModel
from keras import Input
from keras.initializers import GlorotNormal, Zeros
import keras
#from keras import backend as K
try:
    from keras.regularizers import l2
except:
    from keras.regularizers import L2 as l2
else:
    pass
if keras.backend.backend() == 'tensorflow':
    import tensorflow as tf
    backend = tf
else:
    import torch
    backend = torch

import numpy as np
import random
import os 
thicknessA=100


import torch.utils.data as data_utils

from time import time

def collate_function(dataL):
    result =[]
    for i in range(len(dataL[0])):
        result.append(np.concatenate([data[i][np.newaxis,:] for data in dataL]))
    return result

NoneType = type(None)

class MultiHeadAttention(keras.layers.MultiHeadAttention):
    def __init__(self,*args,isAS=False,beta=1,**kwargs):
        self.isAS = isAS
        self.beta = beta
        super(MultiHeadAttention,self).__init__(*args,**kwargs)
    def build(self,query_shape,value_shape,key_shape=None,):
        tmp = super().build(query_shape,value_shape,key_shape)
        if self.beta!=1:
            for W in [self.value_dense,self.output_dense]:
                for w in W.weights:
                    w.assign(w*self.beta)
        return tmp
    def compute_output_shape(
        self,
        query_shape,
        value_shape,
        key_shape=None,
    ):
        if key_shape is None:
            key_shape = value_shape

        if query_shape[-1] != value_shape[-1]:
            raise ValueError(
                "The last dimension of `query_shape` and `value_shape` "
                f"must be equal, but are {query_shape[-1]}, {value_shape[-1]}. "
                "Received: query_shape={query_shape}, value_shape={value_shape}"
            )

        if value_shape[1:-1] != key_shape[1:-1]:
            raise ValueError(
                "All dimensions of `value` and `key`, except the last one, "
                f"must be equal. Received: value_shape={value_shape} and "
                f"key_shape={key_shape}"
            )
        if self.isAS:
            if self._output_shape:
                return (query_shape[0], query_shape[1], self._output_shape),(query_shape[0], self._num_heads, query_shape[1], key_shape[1]) 
            return query_shape, (query_shape[0], self._num_heads, query_shape[1], key_shape[1]) 
        if self._output_shape:
            return query_shape[:-1] + self._output_shape
        return query_shape
class Sum(keras.Layer):
    def call(self, x,**kwargs):
        if keras.backend.backend() == 'tensorflow':
            return tf.reduce_sum(x,**kwargs)
        else:
            return x.sum(**kwargs)
        #return K.sum(x,**kwargs)

class Clip(keras.Layer):
    def call(self, x,xmin=0,xmax=1,):
        if keras.backend.backend() == 'tensorflow':
            return tf.clip(x,xmin,xmax)
        else:
            return torch.clip(x,xmin,xmax)
        #return K.sum(x,**kwargs)
class Exp(keras.Layer):
    def call(self, x,**kwargs):
        if keras.backend.backend() == 'tensorflow':
            return tf.exp(x,**kwargs)
        else:
            return torch.exp(x,**kwargs)
        #return K.sum(x,**kwargs)

class LOG1EXP(keras.Layer):
    def call(self, x,**kwargs):
        if keras.backend.backend() == 'tensorflow':
            return tf.log(tf.exp(x,**kwargs)+1)
        else:
            return torch.log(torch.exp(x,**kwargs)+1)
        #return K.sum(x,**kwargs)

def embedding(inputs,embedding_dim,N=10000):
    omega=1/(N**(np.arange(0,embedding_dim,2)/embedding_dim))
    omega=omega.reshape(1,1,embedding_dim//2)
    omega = tf.constant(omega,dtype=tf.float32)
    sin = tf.math.sin(inputs*omega)
    cos = tf.math.cos(inputs*omega)
    return tf.concat([sin,cos],axis=-1)
def feedForward(inputs,key_dim,activation='relu',LN=None,Dense0=None,Dense1=None,isPre=False,isSwiGLU=False,name='FF',dropout=0,beta=1,alpha=1,**kwags):
    #silu
    hide_dim = key_dim*4
    if isSwiGLU:
        hide_dim = (key_dim*8)//3
        V = Dense( hide_dim,name=name+'V0',**kwags)
        if beta != 1:
            for w in V.weights:
                w.assign(w.get_value()*beta)
    if isinstance(Dense0,NoneType):
        Dense0=Dense(hide_dim,name=name+'W0',**kwags)
        if beta != 1:
            for w in Dense0.weights:
                w.assign(w.get_value()*beta)
    if isinstance(Dense1,NoneType):
        Dense1=Dense(key_dim,name=name+'W1',**kwags)
        if beta != 1:
            for w in Dense1.weights:
                w.assign(w.get_value()*beta)
    if isinstance(LN,NoneType):
        LN=LayerNormalization(epsilon=1e-6,name=name+'LN')
    if isSwiGLU:
        activation = 'silu'
    if dropout>0:
        inputs = Dropout(dropout)(inputs)
    if isPre:
        if isSwiGLU:
            inputs_N = LN(inputs)
            return Dense1(
                Activation(activation,name=name+'ac'+activation)(
                    Dense0(inputs_N))*
                V(inputs_N)
                )+inputs*alpha
        return (Dense1(
                Activation(activation,name=name+'ac'+activation)(Dense0(LN(inputs))))
                )+inputs*alpha
    else:
        return LN(
            Dense1(
                Activation(activation,name=name+'ac'+activation)(Dense0(inputs))
                )
            +inputs*alpha)

class Model(tfModel):
    def __init__(self,key_dim=64,class_n=1,N=6,M=-1,num_heads=6,input_channels=10,maxTypeN=100,dropout=0.1,regularizers = None,loss='MSE',Type='E-D',withSigma=False,lr=1e-3,normType ='LN',isSwiGLU=False,rms_scaling=False,kernel_initializer= GlorotNormal(),bias_initializer= Zeros(),halfQK=False,jit_compile=False,embInput=None,**kwargs):
        #super(Model, self).__init__()
        if normType=='deepNorm':
            normType='LN'
            deepNorm = True
        else:
            deepNorm = False
        self.key_dim = key_dim
        self.N = N
        self.embInput = embInput
        if M<0:
            M = N
        self.M = N
        self.num_heads = num_heads
        self.class_n = class_n
        self.regularizers = regularizers
        inputs = Input((None,input_channels),name='inputs')
        inputsType = Input((None,input_channels),name ='inputsType')
        mask = Input((None,1),name='mask')
        mask1 = Input((None,1),name='mask1')
        outputs = Input((None,input_channels),name='outputs')
        outputsType = Input((None,input_channels),name='outputsType')
        emb = Embedding(maxTypeN, key_dim)
        
        if keras.backend.backend() == 'tensorflow':
            index = tf.reshape(tf.range(90,90+input_channels,dtype=tf.float32),(1,1,input_channels))
        else:
            index = torch.arange(90,90+input_channels).reshape(1,1,input_channels).float()
        
        inputsFlat = Reshape((-1,1))(inputs)#Input((None,input_channels))
        
        inputsTypeFlat = Reshape((-1,))(inputsType)
        inputsTypeFlatEmb = emb(inputsTypeFlat)
        
        inputsTypeIndex = inputsType*0+index
        inputsTypeIndexFlat = Reshape((-1,))(inputsTypeIndex)
        inputsTypeIndexFlatEmb = emb(inputsTypeIndexFlat)
        
        
        inputsMul = (inputsTypeFlatEmb+inputsTypeIndexFlatEmb)*inputsFlat
        inputsE = Sum()(Reshape((-1,input_channels,key_dim))(inputsMul),axis=2)
        trans = keras.layers.Permute([2,1])
        maskT = trans(mask)
        mask1T = trans(mask1)
        
        
        outputs0 = outputs
        
        outputsFlat = Reshape((-1,1))(outputs)#Input((None,input_channels))
        outputsTypeFlat = Reshape((-1,))(outputsType)
        outputsTypeFlatEmb = emb(outputsTypeFlat)
        outputsTypeIndex = outputsType*0+index
        outputsTypeIndexFlat = Reshape((-1,))(outputsTypeIndex)
        outputsTypeIndexFlatEmb = emb(outputsTypeIndexFlat)
        
        outputsMul = (outputsTypeFlatEmb+outputsTypeIndexFlatEmb)*outputsFlat
        outputsE = Sum()(Reshape((-1,input_channels,key_dim))(outputsMul),axis=2)
        
        inputsE0 = inputsE
        outputsE0 = outputsE
        encoderAtten = []
        decoderAtten = []
        QK_dim = key_dim
        V_dim = key_dim
        if halfQK:
            QK_dim = key_dim//2
            #value_dim = key_dim//2
        
        if normType=='LNPre':
            inputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name='inputE0')(inputsE)
            outputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name='outputE0')(outputsE)
        #print(Type)
        #exit()
        if Type=='E-D':
            if deepNorm:
                alpha_en = 0.81*(N**4*M)**(1/16)
                beta_en  = 0.87*(N**4*M)**(-1/16)
                alpha_de = (3*M)**(1/4)
                beta_de  = (12*M)**(-1/4)
                
            else:
                alpha_en =1
                beta_en = 1
                alpha_de =1
                beta_de = 1
            for i in range(N):
                name=f'encoder{i}'
                #inputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(inputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=False)+inputsE)
                inputsEO = inputsE
                if normType=='LNPre':
                    inputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(inputsE)
                elif normType=='BNPre':
                    inputsE=BatchNormalization(name=name+'BN0')(inputsE)
                
                tmp,atten=MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,isAS=True,name=name+'MH0',beta=beta_en,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(inputsE,inputsE,inputsE,attention_mask=maskT,return_attention_scores=True)
                #print(keras.__path__)
                #=tmps
                
                inputsE = tmp + inputsEO*alpha_en
                if normType=='LN':
                    inputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(inputsE)
                elif normType=='BN':
                    inputsE=BatchNormalization(name=name+'BN0')(inputsE)
                
                inputsE = feedForward(inputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF0',dropout=dropout,alpha=alpha_en,beta=beta_en)
                encoderAtten.append(atten)
            if normType=='LNPre':
                inputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name='inputE-final')(inputsE)
            for i in range(N):
                outputsEO = outputsE
                name=f'decoder{i}'
                if normType=='LN':
                    outputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling)(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE*alpha_de)
                elif normType=='BN':
                    outputsE=BatchNormalization()(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE*alpha_de)
                elif normType=='LNPre':
                    outputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=f'{name}_LN0')(outputsE)
                    tmp = MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)
                    outputsE = tmp + outputsEO*alpha_de
                elif normType=='BNPre':
                    outputsE=BatchNormalization(name=f'{name}_BN0')(outputsE)
                    tmp = MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)
                    outputsE = tmp + outputsEO*alpha_de
                
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF0',dropout=dropout,beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer,alpha=alpha_de)
                
                outputsEO = outputsE
                if normType=='LNPre':
                    outputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling)(outputsE)
                
                tmp,atten=MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,isAS=True,name=name+'_MHA1',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=True)
                
                outputsE = tmp+outputsEO*alpha_de
                if normType=='LN':
                    outputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(outputsE)
                elif normType=='BN':
                    outputsE = BatchNormalization()(outputsE)
                
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF1',dropout=dropout,beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer,alpha=alpha_de)
                decoderAtten.append(atten)
        if Type=='E-D-Share':
            if deepNorm:
                alpha_en =0.81*(N**4*M)**(1/16)
                beta_en = 0.87*(N**4*M)**(-1/16)
                alpha_de = (3*M)**(1/4)
                beta_de = (12*M)**(-1/4)
                
            else:
                alpha_en =1
                beta_en = 1
                alpha_de =1
                beta_de = 1
            for i in range(N):
                name=f'encoder{i}'
                #inputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(inputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=False)+inputsE)
                inputsEO = inputsE
                if normType=='LNPre':
                    inputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(inputsE)
                elif normType=='BNPre':
                    inputsE=BatchNormalization(name=name+'BN0')(inputsE)
                
                tmp,atten=MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,isAS=True,name=name+'MH0',beta=beta_en,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(inputsE,inputsE,inputsE,attention_mask=maskT,return_attention_scores=True)
                #print(keras.__path__)
                #=tmps
                
                inputsE = tmp + inputsEO*alpha_en
                if normType=='LN':
                    inputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(inputsE)
                elif normType=='BN':
                    inputsE=BatchNormalization(name=name+'BN0')(inputsE)
                
                inputsE = feedForward(inputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF0',dropout=dropout,alpha=alpha_en)
                encoderAtten.append(atten)
            if normType=='LNPre':
                inputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name='inputE-final')(inputsE)
            for i in range(N):
                outputsEO = outputsE
                name=f'decoder{i}'
                if normType=='LN':
                    outputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling)(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE*alpha_de)
                elif normType=='BN':
                    outputsE=BatchNormalization()(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE*alpha_de)
                elif normType=='LNPre':
                    outputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=f'{name}_LN0')(outputsE)
                    tmp = MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)
                    outputsE = tmp + outputsEO*alpha_de
                elif normType=='BNPre':
                    outputsE=BatchNormalization(name=f'{name}_BN0')(outputsE)
                    tmp = MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,name=f'{name}_MHA0',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)
                    outputsE = tmp + outputsEO*alpha_de
                
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF0',dropout=dropout,beta=beta_de,alpha=alpha_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)
                
                outputsEO = outputsE
                if normType=='LNPre':
                    outputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling)(outputsE)
                
                tmp,atten=MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,isAS=True,name=name+'_MHA1',beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(outputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=True)
                
                outputsE = tmp+outputsEO*alpha_de
                if normType=='LN':
                    outputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(outputsE)
                elif normType=='BN':
                    outputsE = BatchNormalization()(outputsE)
                
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF1',dropout=dropout,beta=beta_de,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer,alpha=alpha_de)
                decoderAtten.append(atten)
        
        elif Type=='EOnly':
            if deepNorm:
                alpha_en =(2*N)**0.25
                beta_en = (8*N)**(-0.25)
                alpha_de = (3*M)**(1/4)
                beta_de = (12*M)**(-1/4)
                
            else:
                alpha_en =1
                beta_en = 1
                alpha_de =1
                beta_de = 1
            inputsN = inputsE.shape[1]
            outputsN = outputsE.shape[1]
            inputsE  = Concatenate(axis=1)([inputsE,outputsE])
            maskT = Concatenate(axis=2)([maskT,mask1T])
            for i in range(N):
                name=f'encoder{i}'
                #inputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(inputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=False)+inputsE)
                inputsEO = inputsE
                if normType=='LNPre':
                    inputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(inputsE)
                elif normType=='BNPre':
                    inputsE=BatchNormalization(name=name+'BN0')(inputsE)
                
                tmp,atten=MultiHeadAttention(num_heads,QK_dim,V_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,isAS=True,name=name+'MH0',beta=beta_en,kernel_initializer=kernel_initializer,bias_initializer=bias_initializer)(inputsE,inputsE,inputsE,attention_mask=maskT,return_attention_scores=True)
                #print(keras.__path__)
                #=tmps
                
                inputsE = tmp + inputsEO*alpha_en
                if normType=='LN':
                    inputsE=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name=name+'LN0')(inputsE)
                elif normType=='BN':
                    inputsE=BatchNormalization(name=name+'BN0')(inputsE)
                
                inputsE = feedForward(inputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers,LN=LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling),isSwiGLU=isSwiGLU,isPre='Pre' in normType,name=name+'FF0',dropout=dropout,alpha=alpha_en)
                encoderAtten.append(atten)
                decoderAtten.append(atten[:,inputsN:,inputsN:])
            outputsE = inputsE[:,inputsN:]
            inputsE = inputsE[:,:inputsN]   
            if normType=='LNPre':
                inputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling,name='inputE-final')(inputsE)
        if Type=='E-DD':
            for i in range(N//2):
                inputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(inputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=False)+inputsE)
                inputsE = feedForward(inputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
            for i in range(N):
                outputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE)
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                tmp,atten=MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=True)
                outputsE = LayerNormalization(epsilon=1e-6)(tmp+outputsE)
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
        elif Type=='ED':
            print('ED')
            #exit()
            maskM=mask1T*tf.transpose(maskT,(0,2,1))
            for i in range(N):
                inputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(inputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=False)+inputsE)
                inputsE = feedForward(inputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                
                outputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE)
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                
                inputsE=LayerNormalization(epsilon=1e-6)(MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(inputsE,outputsE,outputsE,attention_mask= maskM ,return_attention_scores=False)+inputsE)
                inputsE = feedForward(inputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                
                tmp,atten=MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=True)
                outputsE = LayerNormalization(epsilon=1e-6)(tmp+outputsE)
                outputsE = feedForward(outputsE,key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
        elif Type=='EDSAME':
            print('EDSAME')
            #exit()
            for i in range(N):
                MHA= MultiHeadAttention(num_heads,key_dim,key_dim,dropout=dropout,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                LN = LayerNormalization(epsilon=1e-6)
                
                LNIN = LayerNormalization(epsilon=1e-6)
                Dense0 = Dense(key_dim*4,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                Dense1 = Dense(key_dim,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
                
                inputsE=LN(MHA(inputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=False)+inputsE)
                inputsE = feedForward(inputsE,key_dim,LN=LNIN,Dense0=Dense0,Dense1=Dense1)
                
                outputsE=LN(MHA(outputsE,outputsE,outputsE,attention_mask=mask1T  ,return_attention_scores=False)+outputsE)
                outputsE = feedForward(outputsE,key_dim,LN=LNIN,Dense0=Dense0,Dense1=Dense1)
                #inputsE = feedForward(outputsE,key_dim,LN=LNIN,Dense0=Dense0,Dense1=Dense1)
                
                inputsE=LN(MHA(inputsE,outputsE,outputsE,attention_mask=mask  ,return_attention_scores=False)+inputsE)
                inputsE = feedForward(inputsE,key_dim,LN=LNIN,Dense0=Dense0,Dense1=Dense1)
                tmp,atten=MHA(outputsE,inputsE,inputsE,attention_mask=maskT  ,return_attention_scores=True)
                outputsE= LN(tmp+outputsE)
                outputsE = feedForward(outputsE,key_dim,LN=LNIN,Dense0=Dense0,Dense1=Dense1)
        
        
        if normType=='LNPre':
            outputsE = LayerNormalization(epsilon=1e-6,rms_scaling=rms_scaling)(outputsE)
        
        if dropout>0.000000:
            outputsE = Dropout(dropout)(outputsE)
        DenseOut = Dense(class_n,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
        outputs = DenseOut(outputsE)#/key_dim**0.5
        if withSigma:
            print('***********withSigma**********')
            #outputsSigma = Clip()(Exp()(Dense(class_n,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE)),xmin=1e-6,xmax=1e12)
            DenseOutSigma = Dense(class_n,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)
            outputsSigma = Activation('softplus')(DenseOutSigma(outputsE))
            #exp = Exp()(Dense(class_n,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE))
            #outputsSigma= exp/(1+exp)*
            
            #outputsSigma = Activation('sigmoid')(
            #    Dense(class_n,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(
            #        outputsE
            #        )
            #    )*5
            #outputsSigma=Dense(class_n,kernel_regularizer=self.regularizers,bias_regularizer=self.regularizers)(outputsE)
            #outputsSigma = outputsSigma*outputsSigma+1e-9
            outputs =Concatenate(axis=-1) ([outputs,outputsSigma])
        super(Model,self).__init__(inputs=[inputs,inputsType,mask,outputs0,outputsType,mask1],outputs=outputs)#inputsPos
        #β1 = 0.9, β2 = 0.95, eps = 10.5
        if not jit_compile:
            jit_compile = 'auto'
        self.compile(loss=loss, optimizer=keras.optimizers.AdamW(learning_rate=lr,beta_1=0.9,beta_2=0.98,epsilon=1e-9,),metrics=[huber,MSE],jit_compile=jit_compile)
        self.atten = tfModel(inputs=[inputs,inputsType,mask,outputs0,outputsType,mask1],outputs=atten)
        self.inputsE0 = tfModel(inputs=[inputs,inputsType,mask,outputs0,outputsType,mask1],outputs=inputsE0)
        self.outputsE0 = tfModel(inputs=[inputs,inputsType,mask,outputs0,outputsType,mask1],outputs=outputsE0)
        self.inputsE = tfModel(inputs=[inputs,inputsType,mask,outputs0,outputsType,mask1],outputs=inputsE)
        self.outputsE = tfModel(inputs=[inputs,inputsType,mask,outputs0,outputsType,mask1],outputs=outputsE)
        
        self.decoderAttenL = decoderAtten
        self.encoderAttenL = encoderAtten
        self.inputsL = [inputs,inputsType,mask,outputs0,outputsType,mask1]
    def compilreAtten(self):
        self.encoderAtten = tfModel(inputs=self.inputsL,outputs=self.encoderAttenL)
        self.decoderAtten = tfModel(inputs=self.inputsL,outputs=self.decoderAttenL)
    def Predict(self,c=None,TC=None,cSTD=None,g=None,TG=None,gSTD=None,rf=None,timeL=None,p=None,rfSTD=None,vs0=None,Z=np.arange(150,dtype='float32'),vs0STD=None,ST=0.,STDSTD=-1.,CT=0.,CTSTD=-1.,kappa=0.,kappaSTD=-1.):
        inputL =[]
        outputL = []
        embInput = self.embInput
        if c is not None:
            cN = c
            if cSTD is None:
                cSTD = -np.ones_like(c)
            if len(c.shape)==1:
                cN = cN[np.newaxis]
                TC = TC[np.newaxis]
                cSTD = cSTD[np.newaxis]
            cInput =[cN[:,:,np.newaxis],np.stack([TC,cSTD],axis=-1),'c']
            print(cInput[0].shape,cInput[1].shape,cInput[2])
            inputL=inputL+(cInput)
        if g is not None:
            gN = g
            if gSTD is None:
                gSTD = -np.ones_like(g)
            if len(g.shape)==1:
                gN = gN[np.newaxis]
                TG = TG[np.newaxis]
                gSTD = gSTD[np.newaxis]
            gInput =[gN[:,:,np.newaxis],np.stack([TG,gSTD],axis=-1),'g']
            inputL=inputL+(gInput)
        if rf is not None:
            rfN = rf
            if p is None:
                p = np.zeros_like(rf)+0.06*110
            if isinstance(p,float):
                p = np.zeros_like(rf)+p
            if rfSTD is None:
                rfSTD = -np.ones_like(rf)
                
            if len(rf.shape)==1:
                rfN = rfN[np.newaxis]
                timeL = timeL[np.newaxis]
                p = p[np.newaxis]
                rfSTD = rfSTD[np.newaxis]
            rfInput =[rfN[:,:,np.newaxis],np.stack([timeL,p,rfSTD],axis=-1),'rf']
            inputL=inputL+(rfInput)
        if vs0 is None:
            vs0 = np.zeros_like(Z)
        if vs0STD is None:
            vs0STD = -np.ones_like(vs0)
        vs0N = vs0
        if len(vs0N.shape)==1:
            vs0N = vs0N[np.newaxis]
            vs0STD = vs0STD[np.newaxis]
        ZN = Z
        if len(ZN.shape)==1:
            ZN = ZN[np.newaxis]
        vsOuput =[vs0N[:,:,np.newaxis],np.stack([ZN,vs0STD],axis=-1),'vs']
        outputL=outputL+(vsOuput)
        
        
        if isinstance(ST,float):
            ST = np.zeros(ZN.shape[0])+ST
            STDSTD = np.zeros(ZN.shape[0])+STDSTD
        
        if len(ST.shape)==1:
            ST = ST[np.newaxis]
            STDSTD = STDSTD[np.newaxis]
        STOutput =[ST[:,:,np.newaxis],np.stack([STDSTD,],axis=-1),'sediment_thickness']
        outputL=outputL+(STOutput)
        
        if isinstance(CT,float):
            CT = np.zeros(ZN.shape[0])+CT
            CTSTD = np.zeros(ZN.shape[0])+CTSTD
        if len(CT.shape)==1:
            CT = CT[np.newaxis]
            CTSTD = CTSTD[np.newaxis]
        CTOutput =[CT[:,:,np.newaxis],np.stack([CTSTD,],axis=-1),'crust_thickness']
        outputL=outputL+(CTOutput)
        
        if isinstance(kappa,float):
            kappa = np.zeros(ZN.shape[0])+kappa
            kappaSTD = np.zeros(ZN.shape[0])+kappaSTD
        if len(kappa.shape)==1:
            kappa = kappa[np.newaxis]
            kappaSTD = kappaSTD[np.newaxis]
        kappaOutput =[kappa[:,:,np.newaxis],np.stack([kappaSTD,],axis=-1),'kappa']
        outputL=outputL+kappaOutput
        resP = self.predict([
            *embInput(*inputL),
            *embInput(*outputL)
        ])
        vs = resP[:,:-3,0]*embInput.mulA['velocity']
        ST = resP[:,-3,0]*embInput.mulA['depth']
        CT = resP[:,-2,0]*embInput.mulA['depth']
        kappa = resP[:,-1,0]*embInput.mulA['ratio']
        vsSTD = resP[:,:-3,1]*embInput.mulA['velocity']
        STSTD = resP[:,-3,1]*embInput.mulA['depth']
        CTSTD = resP[:,-2,1]*embInput.mulA['depth']
        kappaSTD = resP[:,-1,1]*embInput.mulA['ratio']
        if len(c.shape)==1: 
            vs = vs[0]
            ST = ST[0]
            CT = CT[0]
            kappa = kappa[0]
            vsSTD = vsSTD[0]
            STSTD = STSTD[0]
            CTSTD = CTSTD[0]
            kappaSTD = kappaSTD[0]
            ZN = ZN[0]
        return ZN,vs,ST,CT,kappa,vsSTD,STSTD,CTSTD,kappaSTD
        
        

emb_typeList=['zero','one','c','g','rf','rfs','vs','e','vdss','time','depth','p','velocity','water_thickness','sediment_thickness','crust_thickness','ratio','kappa']
emb_paraD = {'c':['time','velocity'],'g':['time','velocity'],'e':['time','ratio'],'vdss':['time','p'],'rf':['time','p','ratio'],'rfs':['time','p'],'vs':['depth','velocity'],'water_thickness':['depth'],'sediment_thickness':['depth'],'crust_thickness':['depth'],'kappa':['ratio','ratio']}
emb_typeD ={'c':'velocity','g':'velocity','e':'ratio','vs':'velocity','rf':'ratio','rfs':'ratio','vdss':'ratio','water_thickness':'depth','sediment_thickness':'depth','crust_thickness':'depth','kappa':'ratio'}
emb_mulA =  {'velocity':1,'time':40,'depth':100,'p':10,'ratio':1}

class Embeddings:
    def __init__(self,input_channels=10,typeList = emb_typeList,typeD = emb_typeD,mulA = emb_mulA,paraD = emb_paraD ): 
        self.input_channels = input_channels#np.sum(data.shape[-1]for data in args[::2]) 
        self.typeList = typeList
        self.typeD = typeD
        self.mulA = mulA
        self.paraD = paraD
    def __call__(self,*args,maskRatio=0.0,mask0 = [],mustTypeL=['c','water_thickness'],typeL =['c','g','rf','e','rfs','vdss','water_thickness','sediment_thickness','crust_thickness'],KL = [1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,6,7,7,8,8,9,9]):
        
        N = self.input_channels
        
        iL =  np.arange(len(args)//3).tolist()
        
        DataL=[]
        TypeIndexL = []
        MaskL =[]
        for j in range(args[0].shape[0]):
            dataL = []
            typeIndexL = []
            #posL = []
            #CI = 0
            maskL=[]
            if maskRatio>0.0000001:
                K =  random.choice(KL)
                usedTypeL = random.sample(typeL,K)+mustTypeL
                if 'c' not in usedTypeL and 'g' not in usedTypeL and 'e' not in usedTypeL and 'rf' not in usedTypeL:
                    usedTypeL.append(random.choice(['c','g','e','rf']))
            for i in iL:
                #CI = 0
                
                data = args[3*i][j]
                para = args[3*i+1][j]
                
                typeName = args[3*i+2]
                baseName = self.typeD[typeName]
                typeNameIndex = self.typeList.index(typeName)
                baseNameIndex = self.typeList.index(baseName)
                
                paraL = self.paraD[typeName]
                paraLIndex = [self.typeList.index(para) for para in paraL]
                
                
                dataNew = np.zeros((data.shape[0],N))
                typeIndexNew = np.zeros((data.shape[0],N)).astype('int')+1
                dataNew[:,0] = 1
                typeIndexNew[:,0] = typeNameIndex
                dataNew[:,1] = data[:,0]/self.mulA[baseName]
                typeIndexNew[:,1] = baseNameIndex
                for k in range(min(len(paraL),para.shape[-1])):
                    dataNew[:,k+2] = para[:,k]/self.mulA[paraL[k]]
                    typeIndexNew[:,k+2] = paraLIndex[k]
                dataNew = np.where(np.isnan(dataNew),0,dataNew)
                dataL.append(dataNew)
                typeIndexL.append(typeIndexNew)
                mask = 1+np.zeros((data.shape[0]))
                if maskRatio>0.0000001:
                    if args[3*i+2] in usedTypeL:
                        if args[3*i+2] in ['c','g','e','rf','vs']:
                            mask = np.where(np.random.rand(mask.shape[0])>maskRatio,mask,0)
                        else:
                            mask[:] = 1
                    else:
                        mask[:] = 0
                mask = np.where(np.isnan(data).sum(axis=1)>0,0,mask)
                maskL.append(mask)
            data = np.concatenate(dataL,axis=0)
            typeIndex = np.concatenate(typeIndexL,axis=0)
            mask = np.concatenate(maskL)[:,np.newaxis]
            DataL.append(data)
            TypeIndexL.append(typeIndex)
            MaskL.append(mask)
        if len(mask0)>0:
            MaskL=mask0
        return np.array(DataL),np.array(TypeIndexL),np.array(MaskL)

embedding_default = Embeddings()
def huber(y_true, y_pred,delta=0.05):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
    else:
        weight = 1.0
    error = y_true - y_pred
    error = backend.where(backend.abs(error)<delta,0.5*backend.square(error),delta*(backend.abs(error)-0.5*delta))
    W = backend.where(y_true>900,0.0, weight)
    W=W/backend.mean(W)
    return backend.mean(error*W)
def withSigma(y_true, y_pred,delta=3.0):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if isinstance(y_true,torch.Tensor):
        backend = torch
    else:
        backend = np
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
        #weight = weight /K.mean(weight)
    else:
        weight = 1.0
    error = (y_true - y_pred)/y_sigma
    Sigma = backend.log(y_sigma)
    error = backend.where(backend.abs(error)<delta,0.5*backend.square(error),delta*(backend.abs(error)-0.5*delta))
    W = backend.where(y_true>900,0.0,weight)
    W=W/backend.mean(W)
    return backend.mean(error*W)+backend.mean(Sigma*W)

def withSigma0(y_true, y_pred,delta=3):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
        #weight = weight /K.mean(weight)
    else:
        weight = 1.0
    y_sigma0 = 0.1
    error = (y_true - y_pred)/y_sigma0
    Sigma = backend.square(y_sigma/y_sigma0-1)
    error = backend.where(backend.abs(error)<delta,0.5*backend.square(error),delta*(backend.abs(error)-0.5*delta))
    W = backend.where(y_true>900,0.0,weight)
    W=W/backend.mean(W)
    return backend.mean(error*W)+backend.mean(Sigma*W)
def MSE(y_true, y_pred):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
    else:
        weight = 1.0
    W = backend.where(y_true>900,0.0,weight)
    W=W/backend.mean(W)
    return backend.mean(backend.square(y_true - y_pred)*W)

lossD = {'MSE':MSE,'huber':huber,'withSigma':withSigma,'l1':'l1'}#,'withSigmaShift':DynamicCustomLoss()}
